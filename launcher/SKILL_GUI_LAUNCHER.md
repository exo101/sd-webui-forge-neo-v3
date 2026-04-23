# SD WebUI Forge GUI 启动器 — 搭建实操 Skill

## 项目概述

为 SD WebUI Forge 整合包搭建一个 PyQt6 GUI 启动器，功能参考 SimpAI Launcher 和秋叶启动器风格。

---

## 技术栈

- **UI 框架**: PyQt6
- **打包工具**: PyInstaller
- **依赖**: psutil（硬件监控）、PyYAML（配置文件）
- **Python**: 使用整合包自带的 Python，无需用户额外安装

---

## 项目结构

```
launcher/
├── main.py                  # 入口，创建 QApplication
├── build.py                 # PyInstaller 打包脚本
├── requirements.txt
├── core/
│   ├── paths.py             # 统一路径管理（兼容 exe 和源码运行）
│   ├── config.py            # JSON 配置读写（路径存相对路径）
│   ├── launcher.py          # 构建启动参数、生成 bat、管理进程
│   ├── env_checker.py       # 环境检测（Python/Git/CUDA/系统依赖）
│   └── extension_manager.py # 插件管理（git 操作、更新、安装）
└── gui/
    ├── theme.py             # 全局颜色变量和 QSS 样式
    ├── main_window.py       # 主窗口（侧边栏导航 + QTabWidget）
    ├── tab_launch.py        # 主控台（启动按钮、状态卡片）
    ├── tab_settings.py      # 参数设置（所有启动参数 checkbox）
    ├── tab_paths.py         # 路径配置（多路径添加/删除/显示弹窗）
    ├── tab_extensions.py    # 插件管理（表格、检测更新、安装）
    ├── tab_env.py           # 环境检测（系统环境 + Python 依赖）
    ├── tab_log.py           # 运行日志（高亮、跳转错误、复制）
    ├── tab_proxy.py         # 网络代理设置
    └── hw_monitor.py        # 底部硬件监控状态栏
```

---

## 核心实现要点

### 1. 路径管理（最重要）

```python
# core/paths.py
def get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        # PyInstaller 打包后，sys.argv[0] 是 exe 路径
        raw = sys.argv[0]
        # 修正 Windows 盘符后缺反斜杠：G:foo -> G:\foo
        if len(raw) >= 2 and raw[1] == ":" and (len(raw) == 2 or raw[2] not in ("/", "\\")):
            raw = raw[:2] + "\\" + raw[2:]
        return os.path.dirname(os.path.abspath(raw))
    else:
        # 源码运行：从 __file__ 推导项目根目录
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

**关键点**：
- 打包 exe 和源码运行用不同方式定位根目录
- 配置文件保存路径时存**相对路径**，加载时转绝对路径，换盘符/换电脑不失效
- U 盘场景：盘符会变，所以绝对不能硬编码盘符

### 2. 启动参数构建

```python
# core/launcher.py
def build_bat(args: list[str], proxy: str = "", skip_update: bool = False) -> str:
    def quote(a: str) -> str:
        if a.startswith('"') and a.endswith('"'):
            return a
        if " " in a or (len(a) > 1 and a[1] == ":") or "\\" in a:
            # 路径末尾有反斜杠时需要补一个，否则 cmd.exe 会把 \" 当转义
            suffix = "\\" if a.endswith("\\") else ""
            return f'"{a}{suffix}"'
        return a
    cmd_args = " ".join(quote(a) for a in args)
    # ...生成 bat 文件内容
```

**关键点**：
- 所有包含盘符或反斜杠的路径参数都要加引号
- 路径末尾有 `\` 时要补成 `\\`，否则 `"path\"` 中的 `\"` 会被 cmd 解析为转义引号
- 生成临时 bat 文件，用 `cmd.exe /c` 执行，用 `gbk` 编码写入

### 3. 主窗口布局

```python
# gui/main_window.py
# 结构：顶部标题栏 + 左侧导航 + 右侧内容 + 底部状态栏 + 底部硬件监控
# 左侧导航用 QPushButton(checkable=True) 模拟 tab 切换
# 右侧内容用 QTabWidget 但隐藏 tabBar()
```

**关键点**：
- 侧边栏用 `QPushButton` + `setCheckable(True)` 实现，比 `QListWidget` 更灵活
- 内容区用 `QTabWidget` 但 `tabBar().hide()`，通过侧边栏按钮控制 `setCurrentIndex()`
- 快捷键用 `QShortcut`：Ctrl+1~7 切换 tab，Ctrl+W 关闭

### 4. 异步操作（防 UI 冻结）

所有耗时操作都用 `QThread`：

```python
class CheckWorker(QThread):
    result = pyqtSignal(dict)
    
    def run(self):
        data = {...}  # 耗时操作
        self.result.emit(data)  # 通过信号回到主线程更新 UI

# 使用
self._worker = CheckWorker()
self._worker.result.connect(self._on_result)
self._worker.start()

# 清理（重要！防内存泄漏）
def _on_result(self, data):
    # 处理结果...
    if self._worker:
        self._worker.deleteLater()
        self._worker = None
```

**关键点**：
- Worker 完成后必须调用 `deleteLater()` 并置 `None`，否则内存泄漏
- 关闭窗口时要断开信号连接再 stop worker，防止访问已销毁的 UI 对象
- `hw_monitor.py` 里用 `try/except RuntimeError` 保护 `isRunning()` 调用，防止 C++ 对象已删除的崩溃

### 5. 插件管理

```python
# core/extension_manager.py
def update_extension(info: ExtInfo, proxy="", mirror="") -> tuple[bool, str]:
    # 三级降级策略：
    # 1. git pull --rebase（优先）
    # 2. rebase 失败 -> git pull --no-rebase（merge）
    # 3. merge 失败 -> git fetch + git reset --hard（强制同步）
    
    # stash 本地修改
    has_changes = bool(_git(["status", "--porcelain"], path)[1].strip())
    if has_changes:
        stash_ok = _git(["stash"], path)[0] == 0
    
    # ... 拉取逻辑 ...
    
    # reset --hard 后不能 stash pop（会造成冲突）
    if has_changes and stash_ok and not force_reset:
        _git(["stash", "pop"], path)
```

**关键点**：
- GitHub 镜像（ghproxy 系列）的 URL 格式是 `https://ghproxy.com/https://github.com/...`，不是替换域名
- git 代理用 `-c http.proxy=...` 参数注入，比环境变量更可靠
- `reset --hard` 后不能再 `stash pop`，否则会把旧修改应用到干净的工作树上

### 6. 环境检测

```python
# core/env_checker.py
# pip 包名和 import 名不一致时需要映射
PIP_INSTALL_NAME = {
    "open_clip":   "open-clip-torch",  # import open_clip，但 pip install open-clip-torch
    "k_diffusion": "k-diffusion",
}

# 批量检测用单个子进程，避免串行启动 N 个进程
def check_all_packages() -> list[dict]:
    script = "import importlib.metadata as _m\n"
    for pkg in REQUIRED_PACKAGES:
        script += f"try:\n    print('{pkg}=' + _m.version('{pkg}'))\nexcept:\n    print('{pkg}=__MISSING__')\n"
    code, out = _run([PYTHON_EXE, "-c", script])
    # 解析输出...
```

### 7. 日志高亮

```python
# gui/tab_log.py
class LogHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text: str):
        import re
        for pattern, fmt in self._rules:
            for m in re.finditer(pattern, text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)
```

**关键点**：
- 继承 `QSyntaxHighlighter`，重写 `highlightBlock`
- 在 `QPlainTextEdit` 创建后传入 `document()` 初始化

### 8. 打包

```python
# build.py
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",          # 单文件 exe
    "--windowed",         # 无控制台
    "--name", "launcher",
    "--exclude-module", "torch",      # 排除大包，避免打出 2GB+ 的 exe
    "--exclude-module", "numpy",
    "--exclude-module", "matplotlib",
    # ...
    "main.py",
]
```

**关键点**：
- 必须用 `--exclude-module` 排除 torch、numpy 等大包，否则 exe 会有几 GB
- 开发阶段用 bat 直接运行源码，不需要每次打包
- `--onedir` 模式打包快，`--onefile` 模式适合发布

---

## 常见坑

| 问题 | 原因 | 解决 |
|------|------|------|
| exe 运行时路径缺反斜杠 `G:path` | `sys.argv[0]` 在某些情况下返回不带 `\` 的盘符路径 | 手动修正：检测 `raw[1] == ":"` 且 `raw[2]` 不是斜杠时补 `\` |
| bat 里路径参数解析错误 | 路径末尾 `\` 导致 `"path\"` 中 `\"` 被 cmd 当转义 | 末尾有 `\` 时补成 `\\` |
| PyInstaller 打出 2GB+ exe | 整合包 Python 环境里有 torch，被自动打包进去 | `--exclude-module torch` 等 |
| git merge 冲突标记导致 SyntaxError | `git pull --rebase` 失败后文件里留下 `<<<<<<<` 标记 | 用 `git checkout --theirs` 或手动清除冲突标记 |
| BOM 导致 SyntaxError | 文件用 UTF-8 with BOM 保存，Python 解析时报 `U+FEFF` | 用字节读取检测 `EF BB BF` 前缀并去除 |
| pip 安装失败 `No matching distribution` | import 名和 pip 包名不一致 | 维护 `PIP_INSTALL_NAME` 映射表 |
| Worker 线程崩溃 `RuntimeError: wrapped C/C++ object deleted` | Qt 异步删除了 C++ 对象但 Python 引用还在 | `_refresh()` 里用 `try/except RuntimeError` 保护 `isRunning()` |

---

## UI/UX 最佳实践

1. **按钮反馈**：操作后按钮文字/颜色短暂变化（2秒后恢复），用 `QTimer.singleShot`
2. **危险操作确认**：停止、卸载、删除前弹 `QMessageBox.question`
3. **长时间操作**：显示不确定进度条 `setRange(0, 0)`，禁用相关按钮
4. **空状态**：列表为空时显示占位提示文字
5. **搜索反馈**：无结果时改变 label 颜色和文字
6. **loading 状态**：按钮文字改为「⏳ 检测中...」，完成后恢复

---

## 开发工作流

```
日常调试  →  双击 2.GUI启动器.bat（直接跑源码，秒启动）
功能完成  →  双击 4.打包启动器exe.bat 选 2（单文件 exe）
```
