"""环境检测 Tab"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout, QProgressBar,
    QScrollArea, QSizePolicy, QTextEdit, QLineEdit,
    QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QProcess
from .theme import COLORS
from core.env_checker import (
    check_python, check_git, check_cuda, check_vram,
    check_webui_installed, get_webui_version,
    check_all_system_deps,
)


class CheckWorker(QThread):
    result = pyqtSignal(dict)

    def run(self):
        data = {
            "python":   check_python(),
            "git":      check_git(),
            "cuda":     check_cuda(),
            "vram":     check_vram(),
            "webui":    check_webui_installed(),
            "version":  get_webui_version(),
            "sys_deps": check_all_system_deps(),
        }
        self.result.emit(data)


class EnvTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked = False
        self._worker: CheckWorker | None = None
        self._build_ui()
    
    def showEvent(self, event):
        """页面显示时触发"""
        super().showEvent(event)
        # 如果还未检测过，延迟后自动检测
        if not self._checked:
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(300, self._auto_check)
    
    def _auto_check(self):
        """自动检测（仅在未检测过时执行）"""
        if not self._checked and (not self._worker or not self._worker.isRunning()):
            self._force_check()

    def _build_ui(self):
        from PyQt6.QtWidgets import QTabWidget

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(10)

        # ── 顶部标题行 ──
        title_row = QHBoxLayout()
        lbl = QLabel("🔍  环境检测")
        lbl.setStyleSheet(f"color:{COLORS['text_primary']};font-size:18px;font-weight:bold;")
        title_row.addWidget(lbl)
        title_row.addStretch()
        self.btn_refresh = QPushButton("🔄  重新检测")
        self.btn_refresh.clicked.connect(self._force_check)
        title_row.addWidget(self.btn_refresh)
        root.addLayout(title_row)

        # ── 子 Tab：系统环境 / 命令行工具 ──
        self._sub_tabs = QTabWidget()
        self._sub_tabs.setStyleSheet(
            "QTabWidget::pane {"
            "border: 1px solid " + COLORS['border'] + ";"
            "background: " + COLORS['bg_dark'] + ";"
            "border-radius: 0 8px 8px 8px;"
            "}"
            "QTabBar::tab {"
            "background: " + COLORS['bg_dark'] + ";"
            "color: " + COLORS['text_secondary'] + ";"
            "padding: 7px 18px;"
            "border: none;"
            "border-bottom: 2px solid transparent;"
            "font-size: 12px;"
            "}"
            "QTabBar::tab:selected {"
            "color: " + COLORS['text_primary'] + ";"
            "border-bottom: 2px solid " + COLORS['accent'] + ";"
            "font-weight: bold;"
            "}"
            "QTabBar::tab:hover:!selected {"
            "background: " + COLORS['bg_hover'] + ";"
            "color: " + COLORS['text_primary'] + ";"
            "}"
        )
        root.addWidget(self._sub_tabs, 1)

        # ── 子 Tab 1：系统环境 ──
        env_tab = QWidget()
        env_tab.setStyleSheet("background:{bg_dark};".format(bg_dark=COLORS['bg_dark']))
        env_layout = QVBoxLayout(env_tab)
        env_layout.setContentsMargins(12, 12, 12, 12)
        env_layout.setSpacing(8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")

        self.cards_widget = QWidget()
        self.cards_widget.setStyleSheet("background:transparent;")
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.cards_layout.setSpacing(8)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self._build_placeholder()
        self.cards_layout.addStretch()

        scroll.setWidget(self.cards_widget)
        env_layout.addWidget(scroll, 1)
        self._sub_tabs.addTab(env_tab, "  🖥  系统环境  ")

        # ── 子 Tab 2：命令行工具 ──
        cmd_tab = QWidget()
        cmd_tab.setStyleSheet(f"background:{COLORS['bg_dark']};")
        cmd_layout = QVBoxLayout(cmd_tab)
        cmd_layout.setContentsMargins(12, 12, 12, 12)
        cmd_layout.setSpacing(8)

        # 目录选择
        dir_row = QHBoxLayout()
        dir_lbl = QLabel("📁  切换目录：")
        dir_lbl.setStyleSheet(f"color:{COLORS['text_primary']};font-size:12px;")
        dir_row.addWidget(dir_lbl)
        self.dir_combo = QComboBox()
        self.dir_combo.addItems([
            "Python 目录"
        ])
        self.dir_combo.setStyleSheet(f"color:{COLORS['text_primary']};background:{COLORS['bg_input']};border:1px solid {COLORS['border']};border-radius:4px;padding:4px 8px;font-size:12px;")
        dir_row.addWidget(self.dir_combo)
        self.btn_cd = QPushButton("📂  进入目录")
        self.btn_cd.clicked.connect(self._cd_to_directory)
        self.btn_cd.setStyleSheet(f"color:{COLORS['text_primary']};background:{COLORS['bg_hover']};border:1px solid {COLORS['border']};border-radius:4px;padding:4px 12px;font-size:12px;")
        dir_row.addWidget(self.btn_cd)
        dir_row.addStretch()
        cmd_layout.addLayout(dir_row)

        # 常用命令
        cmd_row = QHBoxLayout()
        cmd_lbl = QLabel("⚙️  常用命令：")
        cmd_lbl.setStyleSheet(f"color:{COLORS['text_primary']};font-size:12px;")
        cmd_row.addWidget(cmd_lbl)
        self.cmd_combo = QComboBox()
        self.cmd_combo.addItems([
            "pip 安装包",
            "pip 卸载包",
            "pip 列出依赖",
            "清理缓存垃圾"
        ])
        self.cmd_combo.setStyleSheet(f"color:{COLORS['text_primary']};background:{COLORS['bg_input']};border:1px solid {COLORS['border']};border-radius:4px;padding:4px 8px;font-size:12px;")
        cmd_row.addWidget(self.cmd_combo)
        self.btn_run = QPushButton("▶  执行")
        self.btn_run.clicked.connect(self._run_command)
        self.btn_run.setStyleSheet(f"color:{COLORS['text_primary']};background:{COLORS['bg_hover']};border:1px solid {COLORS['border']};border-radius:4px;padding:4px 12px;font-size:12px;")
        cmd_row.addWidget(self.btn_run)
        cmd_row.addStretch()
        cmd_layout.addLayout(cmd_row)

        # 输出区域
        self.cmd_output = QTextEdit()
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setStyleSheet(f"""
            background:{COLORS['bg_card']};
            color:{COLORS['text_primary']};
            border:1px solid {COLORS['border']};
            border-radius:6px;
            padding:8px;
            font-family:'Consolas','Courier New',monospace;
            font-size:12px;
        """)
        cmd_layout.addWidget(self.cmd_output, 1)

        self._sub_tabs.addTab(cmd_tab, "  💻  命令行工具  ")

    def _build_placeholder(self):
        """构建占位符"""
        placeholder = QLabel("点击「重新检测」开始环境检测...")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(f"color:{COLORS['text_dim']};font-size:13px;padding:40px;")
        placeholder.setObjectName("env_placeholder")
        self.cards_layout.addWidget(placeholder)

    def _clear_cards(self):
        """清空卡片"""
        # 先移除所有项（包括stretch）
        while self.cards_layout.count() > 0:
            item = self.cards_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                # 如果是layout项，也需要清理
                sub_layout = item.layout()
                if sub_layout is not None:
                    self._clear_layout(sub_layout)
    
    def _clear_layout(self, layout):
        """递归清空布局"""
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                sub_layout = item.layout()
                if sub_layout is not None:
                    self._clear_layout(sub_layout)

    def _force_check(self):
        """强制重新检测"""
        if self._worker and self._worker.isRunning():
            return
        
        self._clear_cards()
        loading = QLabel("⏳  正在检测环境...")
        loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:13px;padding:40px;")
        self.cards_layout.insertWidget(0, loading)
        
        self._worker = CheckWorker()
        self._worker.result.connect(self._on_result)
        self._worker.start()

    def _on_result(self, data: dict):
        """检测结果回调"""
        self._clear_cards()
        
        # Python
        python_info = data.get("python", {})
        if isinstance(python_info, bool):
            python_info = {"ok": python_info, "msg": "已安装" if python_info else "未找到"}
        self._add_card("Python", python_info)
        
        # Git
        git_info = data.get("git", {})
        if isinstance(git_info, bool):
            git_info = {"ok": git_info, "msg": "已安装" if git_info else "未找到"}
        self._add_card("Git", git_info)
        
        # CUDA
        cuda_info = data.get("cuda", {})
        if isinstance(cuda_info, bool):
            cuda_info = {"ok": cuda_info, "msg": "已检测到" if cuda_info else "未检测到"}
        elif isinstance(cuda_info, dict):
            # 将CUDA检测结果转换为msg格式
            torch_ver = cuda_info.get("torch", "未知")
            gpu_name = cuda_info.get("gpu", "N/A")
            cuda_available = cuda_info.get("cuda", False)
            if cuda_info.get("ok"):
                cuda_info["msg"] = f"PyTorch {torch_ver} | GPU: {gpu_name}"
            else:
                cuda_info["msg"] = f"CUDA不可用 | PyTorch: {torch_ver}"
        self._add_card("CUDA", cuda_info)
        
        # VRAM
        vram_info = data.get("vram", {})
        if isinstance(vram_info, bool):
            vram_info = {"ok": vram_info, "msg": "正常" if vram_info else "异常"}
        elif isinstance(vram_info, dict):
            # 将VRAM检测结果转换为msg格式
            total_mb = vram_info.get("total_mb", 0)
            gpu_name = vram_info.get("name", "N/A")
            if vram_info.get("ok"):
                vram_info["msg"] = f"{total_mb} MB | {gpu_name}"
            else:
                vram_info["msg"] = "无法检测显存"
        self._add_card("显存", vram_info)
        
        # WebUI - 可能是布尔值，需要转换
        webui_info = data.get("webui", False)
        if isinstance(webui_info, bool):
            webui_info = {"ok": webui_info, "msg": "已安装" if webui_info else "未安装"}
        self._add_card("WebUI", webui_info)
        
        # Version
        version = data.get("version")
        if version:
            self._add_card("版本", {"ok": True, "msg": str(version)})
        
        # System Dependencies - 可能是列表或字典
        sys_deps = data.get("sys_deps")
        if sys_deps:
            if isinstance(sys_deps, list):
                # 如果是列表，遍历每个依赖项
                for dep_info in sys_deps:
                    if isinstance(dep_info, dict):
                        dep_name = dep_info.get("name", "未知依赖")
                        self._add_card(dep_name, dep_info)
            elif isinstance(sys_deps, dict):
                # 如果是字典，按原逻辑处理
                for dep_name, dep_info in sys_deps.items():
                    self._add_card(dep_name, dep_info)
        
        self.cards_layout.addStretch()
        self._checked = True
        
        # 强制刷新UI和布局
        self.cards_widget.updateGeometry()
        self.cards_widget.update()
        self.cards_widget.repaint()

    def _add_card(self, title: str, info):
        """添加检测卡片"""
        # 处理不同类型的info参数
        if isinstance(info, bool):
            info = {"ok": info, "msg": "正常" if info else "异常"}
        elif isinstance(info, str):
            info = {"ok": True, "msg": info}
        elif not isinstance(info, dict):
            info = {"ok": False, "msg": str(info)}
        
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background:{COLORS['bg_card']};
                border-radius:8px;
                border:1px solid {COLORS['border']};
            }}
        """)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # 图标
        icon = QLabel("✅" if info.get("ok") else "❌")
        icon.setStyleSheet("font-size:18px;")
        layout.addWidget(icon)

        # 内容
        content = QVBoxLayout()
        content.setSpacing(4)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color:{COLORS['text_primary']};font-weight:bold;font-size:13px;")
        content.addWidget(title_lbl)

        # 尝试多种可能的消息字段名
        msg = info.get("msg") or info.get("detail") or info.get("message") or info.get("version") or ""
        if msg:
            msg_lbl = QLabel(str(msg))
            msg_lbl.setWordWrap(True)
            msg_lbl.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:11px;")
            content.addWidget(msg_lbl)

        content.addStretch()
        layout.addLayout(content, 1)

        self.cards_layout.addWidget(card)

    def _cd_to_directory(self):
        """切换到指定目录"""
        from core.paths import BASE_DIR
        import subprocess
        
        index = self.dir_combo.currentIndex()
        if index == 0:  # Python 目录
            python_dir = os.path.join(BASE_DIR, "system", "python")
            if os.path.exists(python_dir):
                subprocess.Popen(f'explorer "{python_dir}"')

    def _run_command(self):
        """执行命令"""
        from core.paths import BASE_DIR
        import subprocess
        
        index = self.cmd_combo.currentIndex()
        python_exe = os.path.join(BASE_DIR, "system", "python", "python.exe")
        
        commands = [
            f'"{python_exe}" -m pip install <package_name>',
            f'"{python_exe}" -m pip uninstall <package_name>',
            f'"{python_exe}" -m pip list',
            f'"{python_exe}" -m pip cache purge'
        ]
        
        if index < len(commands):
            self.cmd_output.setText(f"命令模板：\n{commands[index]}\n\n请在命令行中手动替换 <package_name> 为实际的包名")
