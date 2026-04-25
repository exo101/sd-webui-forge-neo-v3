"""主控台 Tab"""
import os
import subprocess
import psutil
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QSizePolicy, QPlainTextEdit, QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, QUrl
from PyQt6.QtGui import QDesktopServices, QFont
from .theme import COLORS
from core.paths import BASE_DIR, WEBUI_DIR
from core.version_manager import check_github_update, update_from_github, get_current_version

WEBUI_MODELS_DIR = os.path.join(WEBUI_DIR, "models")


class GitCheckWorker(QThread):
    """异步检测 WebUI 是否有新版本"""
    result = pyqtSignal(dict)  # {has_update, local, remote, error}

    def run(self):
        git = os.path.join(BASE_DIR, "system", "git", "bin", "git.exe")
        try:
            r_local = subprocess.run([git, "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=5, cwd=WEBUI_DIR,
                creationflags=subprocess.CREATE_NO_WINDOW)
            local = r_local.stdout.strip() if r_local.returncode == 0 else "?"

            subprocess.run([git, "fetch", "origin", "--quiet"],
                capture_output=True, timeout=15, cwd=WEBUI_DIR,
                creationflags=subprocess.CREATE_NO_WINDOW)

            r_remote = subprocess.run([git, "rev-parse", "--short", "origin/HEAD"],
                capture_output=True, text=True, timeout=5, cwd=WEBUI_DIR,
                creationflags=subprocess.CREATE_NO_WINDOW)
            remote = r_remote.stdout.strip() if r_remote.returncode == 0 else "?"

            has_update = bool(local and remote and local != remote and remote != "?")
            self.result.emit({"has_update": has_update, "local": local, "remote": remote, "error": ""})
        except Exception as e:
            self.result.emit({"has_update": False, "local": "?", "remote": "?", "error": str(e)})


class LauncherUpdateCheckThread(QThread):
    """后台检查启动器更新的线程"""
    finished = pyqtSignal(dict)  # 发送检查结果
    
    def run(self):
        result = check_github_update()
        self.finished.emit(result or {})


class LauncherUpdateThread(QThread):
    """后台执行启动器更新的线程"""
    progress = pyqtSignal(str)  # 进度消息
    finished = pyqtSignal(bool, str)  # (成功与否, 消息)
    
    def run(self):
        def callback(msg):
            self.progress.emit(msg)
        
        success, message = update_from_github(progress_callback=callback)
        self.finished.emit(success, message)


class LaunchTab(QWidget):
    sig_launch       = pyqtSignal()
    sig_stop         = pyqtSignal()
    sig_open_browser = pyqtSignal()
    sig_goto         = pyqtSignal(int)   # 跳转到其他 tab
    sig_stop_all     = pyqtSignal()

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.config = config
        self._running = False
        self._git_worker = None
        self._launcher_update_check_thread = None
        self._launcher_update_thread = None
        self._build_ui()
        # 已移除GPU检测和内存检测，环境检测页面已有此功能

    # Stop all processes launched by this launcher (internal helper for outer control)
    def stop_all(self):
        """彻底清理所有WebUI相关进程和资源"""
        import signal
        
        # 1. 停止git检查线程
        try:
            if hasattr(self, "_git_worker") and self._git_worker is not None:
                try:
                    self._git_worker.terminate()
                    self._git_worker.wait(2000)  # 等待最多2秒
                except Exception:
                    pass
                self._git_worker = None
        except Exception:
            pass
        
        # 2. 查找并终止所有Python子进程（WebUI相关）
        try:
            current_pid = os.getpid()  # 当前启动器进程ID
            webui_dir_lower = WEBUI_DIR.lower()
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
                try:
                    pid = proc.info['pid']
                    cmdline = proc.info['cmdline']
                    cwd = proc.info['cwd']
                    
                    # 跳过自己
                    if pid == current_pid:
                        continue
                    
                    # 检查是否是WebUI相关的Python进程
                    is_webui_process = False
                    
                    if cmdline:
                        cmdline_str = ' '.join(cmdline).lower()
                        # 检查命令行是否包含webui目录
                        if webui_dir_lower in cmdline_str:
                            is_webui_process = True
                        # 检查是否是gradio/uvicorn等WebUI服务进程
                        elif any(keyword in cmdline_str for keyword in ['webui.py', 'launch.py', 'gradio', 'uvicorn']):
                            is_webui_process = True
                    
                    if cwd and webui_dir_lower in cwd.lower():
                        is_webui_process = True
                    
                    # 如果是WebUI进程，强制终止
                    if is_webui_process:
                        parent = psutil.Process(pid)
                        # 先终止所有子进程
                        children = parent.children(recursive=True)
                        for child in children:
                            try:
                                child.kill()
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
                        
                        # 再终止父进程
                        try:
                            parent.kill()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            pass
        
        # 3. 清理端口占用
        try:
            port = self.config.get("port", 7869)
            from core.launcher import kill_process_on_port
            if kill_process_on_port(port):
                pass
        except Exception as e:
            pass
        
        # 4. 清理临时文件
        try:
            from core.launcher import cleanup_all_temp_files
            cleanup_all_temp_files()
        except Exception as e:
            pass

    def set_running(self, running: bool):
        """设置运行状态"""
        self._running = running
        
        # 更新按钮状态
        if hasattr(self, 'btn_launch'):
            self.btn_launch.setEnabled(not running)
            if running:
                self.btn_launch.setText("⏳  运行中...")
                self.lbl_hint.setText("WebUI 正在运行中...")
            else:
                self.btn_launch.setText("⚡  启动")
                self.lbl_hint.setText("点击「启动」开始运行 WebUI")
        
        if hasattr(self, 'btn_stop'):
            self.btn_stop.setEnabled(running)
        
        if hasattr(self, 'btn_stop_all'):
            self.btn_stop_all.setEnabled(running)
        
        if hasattr(self, 'btn_browser'):
            self.btn_browser.setEnabled(running)

    def _confirm_stop_all(self):
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要停止所有进程吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.sig_stop_all.emit()

    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")

        content = QWidget()
        content.setStyleSheet(f"background:{COLORS['bg_card']};")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # ── 标题 ──────────────────────────────────────────────
        lbl_title = QLabel("🏠  主控台")
        lbl_title.setStyleSheet(f"color:{COLORS['text_primary']};font-size:18px;font-weight:bold;")
        layout.addWidget(lbl_title)
        lbl_sub = QLabel("欢迎使用 SD WebUI Forge 启动器")
        lbl_sub.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        layout.addWidget(lbl_sub)

        # ── 公告卡片（包含开发者信息）─────────────────────────
        layout.addWidget(self._build_announcement())

        # ── 更新提示横幅（默认隐藏）────────────────────────
        self.update_banner = self._build_update_banner()
        self.update_banner.hide()
        layout.addWidget(self.update_banner)

        # ── 内存警告横幅（默认隐藏）────────────────────────
        self.mem_banner = self._build_mem_banner()
        self.mem_banner.hide()
        layout.addWidget(self.mem_banner)

        # ── 快速启动 ──────────────────────────────────────────
        lbl_quick_start = QLabel("🚀 快速启动")
        lbl_quick_start.setStyleSheet(f"color:{COLORS['text_primary']};font-size:15px;font-weight:bold;margin-top:8px;")
        layout.addWidget(lbl_quick_start)
        layout.addWidget(self._build_launch_buttons())

        # ── 主控台内容容器 ────────────────────────────────────
        self.console_container = self._build_console_area()
        layout.addWidget(self.console_container)

        layout.addStretch()

        scroll.setWidget(content)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    # ── 更新横幅 ──────────────────────────────────────────────

    def _build_announcement(self) -> QFrame:
        """构建公告卡片"""
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtWidgets import QLabel
        
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_dark']};
                border-radius: 10px;
                border: 2px solid {COLORS['accent']}55;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        # 标题行
        title_layout = QHBoxLayout()
        lbl_title = QLabel("📢 重要公告")
        lbl_title.setStyleSheet(f"color:{COLORS['accent_light']};font-weight:bold;font-size:14px;")
        title_layout.addWidget(lbl_title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 主内容区域：左右分栏布局
        main_row = QHBoxLayout()
        main_row.setSpacing(16)

        # 左侧：QQ群图片
        left_col = QVBoxLayout()
        left_col.setSpacing(8)
        
        try:
            img_path = os.path.join(os.path.dirname(__file__), "..", "qq群ai交流群.jpg")
            img_path = os.path.normpath(img_path)
            
            if os.path.exists(img_path):
                lbl_img = QLabel()
                lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # 加载并缩放图片
                pixmap = QPixmap(img_path)
                if not pixmap.isNull():
                    # 限制最大宽度为180px
                    max_width = 180
                    if pixmap.width() > max_width:
                        scaled_pixmap = pixmap.scaledToWidth(max_width, Qt.TransformationMode.SmoothTransformation)
                        lbl_img.setPixmap(scaled_pixmap)
                    else:
                        lbl_img.setPixmap(pixmap)
                    
                    lbl_img.setStyleSheet(f"""
                        background-color: {COLORS['bg_card']};
                        border-radius: 8px;
                        padding: 8px;
                    """)
                    left_col.addWidget(lbl_img)
                    
                    # 图片下方提示
                    lbl_hint = QLabel("扫码加入 AI 交流群")
                    lbl_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    lbl_hint.setStyleSheet(f"""
                        color: {COLORS['text_primary']};
                        font-size: 11px;
                        font-weight: bold;
                        padding-top: 4px;
                    """)
                    left_col.addWidget(lbl_hint)
        except Exception as e:
            lbl_qq = QLabel("💬\n交流群")
            lbl_qq.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_qq.setStyleSheet(f"""
                color: {COLORS['text_secondary']};
                font-size: 12px;
                padding: 40px 20px;
                background-color: {COLORS['bg_card']};
                border-radius: 8px;
            """)
            left_col.addWidget(lbl_qq)
        
        left_col.addStretch()
        main_row.addLayout(left_col)

        # 右侧：公告信息和开发者信息
        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        # 硬件兼容性警告和重要提示
        announcements = [
            ("❌", "不支持 A卡（AMD显卡）", "#ff6b6b"),
            ("❌", "不支持 GTX 10系早期显卡", "#ff6b6b"),
            ("✅", "CUDA 13.0 + PyTorch 2.10 最新环境", COLORS['green']),
            ("⚠️", "使用前务必更新英伟达驱动至最新版本（GeForce Game Ready 驱动程序版本:596.21）", "#ffd93d"),
            ("💡", "旧版 SD WebUI 模型通用，直接迁移 models 目录即可", COLORS['accent']),
            ("🔧", "首次使用请运行「1.安装启动器依赖」脚本安装必要组件", COLORS['accent']),
            ("🚫", "不可将整合包放到重复路径或特殊符号命名下，如：（、）、0、*、&、~", "#ff6b6b")
        ]

        for icon, text, color in announcements:
            row = QHBoxLayout()
            row.setSpacing(6)
            
            lbl_icon = QLabel(icon)
            lbl_icon.setStyleSheet(f"font-size: 12px;")
            row.addWidget(lbl_icon)
            
            lbl_text = QLabel(text)
            lbl_text.setWordWrap(True)
            lbl_text.setStyleSheet(f"""
                color: {color};
                font-size: 12px;
                font-weight: bold;
            """)
            row.addWidget(lbl_text, 1)
            
            right_col.addLayout(row)

        # 分隔线
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setStyleSheet(f"background-color: {COLORS['border']};max-height: 1px;")
        right_col.addWidget(separator1)

        # 开发者信息
        dev_items = [
            ("B站", "哔哩哔哩（鸡肉爱土豆）", "https://space.bilibili.com/403361177"),
            ("GitHub", "exo101", "https://github.com/exo101"),
        ]
        
        for label, value, url in dev_items:
            row = QHBoxLayout()
            row.setSpacing(6)
            
            lbl_label = QLabel(f"{label}:")
            lbl_label.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:11px;min-width:40px;")
            row.addWidget(lbl_label)
            
            if url:
                lbl_value = QLabel(value)
                lbl_value.setStyleSheet(f"color:{COLORS['accent']};font-size:11px;")
                lbl_value.setCursor(Qt.CursorShape.PointingHandCursor)
                
                # 创建自定义点击事件处理
                def make_click_handler(link_url):
                    def handler(event):
                        QDesktopServices.openUrl(QUrl(link_url))
                    return handler
                
                lbl_value.mousePressEvent = make_click_handler(url)
                row.addWidget(lbl_value, 1)
            else:
                lbl_value = QLabel(value)
                lbl_value.setStyleSheet(f"color:{COLORS['text_primary']};font-size:11px;")
                row.addWidget(lbl_value, 1)
            
            right_col.addLayout(row)

        # 分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet(f"background-color: {COLORS['border']};max-height: 1px;")
        right_col.addWidget(separator2)

        # 整合包声明
        disclaimer_text = (
            "此版本整合包通过秋叶aaaki、张吕敏、Haoming02等多位大佬技术总结做出的版本，"
            "不属于任何个人、企业，是非盈利性质的开源软件。"
        )
        lbl_disclaimer = QLabel(disclaimer_text)
        lbl_disclaimer.setWordWrap(True)
        lbl_disclaimer.setStyleSheet(f"""
            color: {COLORS['text_dim']};
            font-size: 10px;
            line-height: 1.4;
        """)
        right_col.addWidget(lbl_disclaimer)

        right_col.addStretch()
        main_row.addLayout(right_col, 1)

        layout.addLayout(main_row)

        return frame

    def _build_console_area(self) -> QFrame:
        """构建主控台内容区域"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_dark']};
                border-radius: 10px;
                border: 1px solid {COLORS['border']};
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # 移除内存信息和状态提示

        return frame

    def _secondary_btn_style(self) -> str:
        """次要按钮样式"""
        return f"""
            QPushButton{{background:{COLORS['bg_card']};color:{COLORS['text_secondary']};
                border:1px solid {COLORS['border']};border-radius:8px;font-size:13px;}}
            QPushButton:hover{{background:{COLORS['bg_hover']};color:{COLORS['text_primary']};}}
            QPushButton:disabled{{background:{COLORS['bg_card']};color:{COLORS['text_dim']};
                border-color:{COLORS['border']};}}
        """

    def _on_stop_click(self):
        """停止按钮点击处理"""
        self.sig_stop.emit()

    def _active_btn_style(self) -> str:
        return f"""
            QPushButton {{
                background: {COLORS['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {COLORS['accent_light']};
            }}
        """

    def _inactive_btn_style(self) -> str:
        return f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {COLORS['bg_hover']};
                color: {COLORS['text_primary']};
            }}
        """

    def _build_update_banner(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{ background:#1a3a1a; border-radius:10px;
                border:1px solid {COLORS['green']}55; }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(4)

        top = QHBoxLayout()
        icon = QLabel("✅")
        icon.setStyleSheet("font-size:18px;")
        top.addWidget(icon)

        self.lbl_update_title = QLabel("WebUI 有新版本可以更新！")
        self.lbl_update_title.setStyleSheet(
            f"color:{COLORS['green']};font-size:14px;font-weight:bold;")
        top.addWidget(self.lbl_update_title)
        top.addStretch()

        btn_close_banner = QPushButton("关闭")
        btn_close_banner.setFixedSize(50, 24)
        btn_close_banner.setStyleSheet(f"""
            QPushButton{{background:transparent;color:{COLORS['text_dim']};
                border:1px solid {COLORS['border']};border-radius:4px;font-size:11px;}}
            QPushButton:hover{{color:{COLORS['text_primary']};}}
        """)
        btn_close_banner.clicked.connect(lambda: self.update_banner.hide())
        top.addWidget(btn_close_banner)
        layout.addLayout(top)

        self.lbl_update_detail = QLabel("")
        self.lbl_update_detail.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:12px;")
        layout.addWidget(self.lbl_update_detail)

        return frame

    # ── 内存警告横幅 ──────────────────────────────────────────

    def _build_mem_banner(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{ background:#2a2a0a; border-radius:10px;
                border:1px solid {COLORS['yellow']}55; }}
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 12, 20, 12)

        icon = QLabel("⚠️")
        icon.setStyleSheet("font-size:18px;")
        layout.addWidget(icon)

        self.lbl_mem_warn = QLabel("")
        self.lbl_mem_warn.setStyleSheet(f"color:{COLORS['yellow']};font-size:12px;")
        self.lbl_mem_warn.setWordWrap(True)
        layout.addWidget(self.lbl_mem_warn, 1)

        return frame

    # ── 快速启动按钮组 ────────────────────────────────────────

    def _build_launch_buttons(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame{{background:{COLORS['bg_dark']};border-radius:10px;
                border:1px solid {COLORS['border']};}}
        """)
        grid_layout = QVBoxLayout(frame)
        grid_layout.setContentsMargins(16, 16, 16, 16)
        grid_layout.setSpacing(10)

        # 第一行：启动按钮 + 检查更新按钮
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self.btn_launch = QPushButton("⚡  启动")
        self.btn_launch.setFixedHeight(60)
        self.btn_launch.setStyleSheet(f"""
            QPushButton{{background:{COLORS['accent']};color:white;border:none;
                border-radius:8px;font-size:13px;font-weight:bold;}}
            QPushButton:hover{{background:{COLORS['accent_light']};}}
            QPushButton:disabled{{background:#3a3a5c;color:{COLORS['text_dim']};}}
        """)
        self.btn_launch.clicked.connect(self.sig_launch.emit)
        row1.addWidget(self.btn_launch, 2)

        # GitHub更新按钮
        self.btn_check_launcher_update = QPushButton("🔄 检查启动器更新")
        self.btn_check_launcher_update.setFixedHeight(60)
        self.btn_check_launcher_update.setStyleSheet(f"""
            QPushButton{{background:#2a7bd5;color:white;border:none;
                border-radius:8px;font-size:12px;font-weight:bold;}}
            QPushButton:hover{{background:#3a8be5;}}
            QPushButton:disabled{{background:#3a3a5c;color:{COLORS['text_dim']};}}
        """)
        self.btn_check_launcher_update.clicked.connect(self._check_launcher_update)
        row1.addWidget(self.btn_check_launcher_update, 1)
        
        grid_layout.addLayout(row1)

        # 第二行：打开界面 + 停止
        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self.btn_browser = QPushButton("🌐  打开 WEB 页面")
        self.btn_browser.setFixedHeight(44)
        self.btn_browser.setEnabled(False)
        self.btn_browser.setStyleSheet(self._secondary_btn_style())
        self.btn_browser.clicked.connect(self.sig_open_browser.emit)
        row2.addWidget(self.btn_browser, 1)

        self.btn_stop = QPushButton("⏹  停止运行")
        self.btn_stop.setFixedHeight(44)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet(f"""
            QPushButton{{background:#3d1f1f;color:{COLORS['red']};
                border:1px solid #5a2020;border-radius:8px;font-size:13px;}}
            QPushButton:hover{{background:#5a2020;}}
            QPushButton:disabled{{background:{COLORS['bg_card']};
                color:{COLORS['text_dim']};border-color:{COLORS['border']};}}
        """)
        self.btn_stop.clicked.connect(self._on_stop_click)
        row2.addWidget(self.btn_stop, 1)

        # Stop all processes (shutdowns everything this launcher may start)
        self.btn_stop_all = QPushButton("停止全部进程")
        self.btn_stop_all.setFixedHeight(44)
        self.btn_stop_all.setEnabled(False)
        self.btn_stop_all.setStyleSheet(f"""
            QPushButton{{background:#2a2a2a;color:{COLORS['red']};
                border:1px solid {COLORS['border']}; border-radius:8px; font-size:13px;}}
            QPushButton:hover{{background:#3a3a3a;}}
        """)
        self.btn_stop_all.clicked.connect(self._confirm_stop_all)
        row2.addWidget(self.btn_stop_all, 1)
        grid_layout.addLayout(row2)

        # 状态行
        self.lbl_hint = QLabel("点击「启动」开始运行 WebUI")
        self.lbl_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_hint.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        grid_layout.addWidget(self.lbl_hint)

        return frame

    def _check_launcher_update(self):
        """检查启动器更新"""
        self.btn_check_launcher_update.setEnabled(False)
        self.btn_check_launcher_update.setText("⏳ 检查中...")
        
        # 创建后台线程
        self._launcher_update_check_thread = LauncherUpdateCheckThread()
        self._launcher_update_check_thread.finished.connect(self._on_launcher_update_check_finished)
        self._launcher_update_check_thread.start()
    
    def _on_launcher_update_check_finished(self, result):
        """启动器更新检查完成回调"""
        self.btn_check_launcher_update.setEnabled(True)
        self.btn_check_launcher_update.setText("🔄 检查启动器更新")
        
        if not result:
            QMessageBox.warning(
                self, 
                "检查失败", 
                "无法连接到GitHub，请检查网络连接\n\n"
                "可能的原因：\n"
                "• 网络连接不稳定\n"
                "• 防火墙或代理阻止了连接\n"
                "• GitHub服务暂时不可用\n\n"
                "建议：\n"
                "• 稍后重试\n"
                "• 检查网络设置\n"
                "• 如持续失败可手动从GitHub下载更新"
            )
            return
        
        if not result.get('has_update'):
            current_ver = result.get('current_version', '未知')
            latest_ver = result.get('latest_version', '未知')
            QMessageBox.information(
                self, 
                "无需更新", 
                f"当前已是最新版本\n版本: {current_ver}"
            )
            return
        
        # 有可用更新
        reply = QMessageBox.question(
            self,
            "发现新版本",
            f"当前版本: {result.get('current_version')}\n"
            f"最新版本: {result.get('latest_version')}\n"
            f"更新时间: {result.get('commit_date')}\n\n"
            f"更新内容:\n{result.get('commit_message')}\n\n"
            f"是否立即更新？\n\n"
            f"注意：更新完成后需要重启启动器",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self._perform_launcher_update()
    
    def _perform_launcher_update(self):
        """执行启动器更新"""
        # 禁用按钮
        self.btn_check_launcher_update.setEnabled(False)
        self.btn_launch.setEnabled(False)
        
        # 创建进度对话框
        self.progress_dialog = QProgressDialog("正在更新启动器...", "取消", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setWindowTitle("更新启动器")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.show()
        
        # 创建更新线程
        self._launcher_update_thread = LauncherUpdateThread()
        self._launcher_update_thread.progress.connect(self._on_launcher_update_progress)
        self._launcher_update_thread.finished.connect(self._on_launcher_update_finished)
        self._launcher_update_thread.start()
    
    def _on_launcher_update_progress(self, message):
        """更新进度回调"""
        self.progress_dialog.setLabelText(message)
    
    def _on_launcher_update_finished(self, success, message):
        """更新完成回调"""
        self.progress_dialog.close()
        self.btn_check_launcher_update.setEnabled(True)
        self.btn_launch.setEnabled(True)
        
        if success:
            QMessageBox.information(
                self, 
                "更新成功", 
                f"{message}\n\n请重启启动器以应用更新！"
            )
        else:
            QMessageBox.critical(self, "更新失败", message)
