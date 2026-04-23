"""主窗口"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from .theme import MAIN_STYLE, COLORS
from .tab_launch import LaunchTab
from .tab_settings import SettingsTab
from .tab_paths import PathsTab
from .tab_env import EnvTab
from .tab_log import LogTab
from .tab_extensions import ExtensionsTab
from .tab_proxy import ProxyTab
from .hw_monitor import HWMonitorBar
from .tab_versions import VersionsTab
from .tab_model_guide import ModelGuideTab
from .tab_plugin_guide import PluginGuideTab
from .tab_resource_summary import ResourceSummaryTab
from core.config import load_config, save_config
from core.launcher import LaunchWorker
from core.paths import BASE_DIR


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.worker: LaunchWorker | None = None

        self.setWindowTitle("SD WebUI Forge 启动器")
        self.setMinimumSize(960, 660)
        self.resize(1060, 740)
        self.setStyleSheet(MAIN_STYLE)
        self._build_ui()
        self._setup_shortcuts()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        root.addLayout(body, 1)

        body.addWidget(self._build_sidebar())
        body.addWidget(self._build_content(), 1)

        root.addWidget(self._build_statusbar())

    def _setup_shortcuts(self):
        from PyQt6.QtGui import QKeySequence, QShortcut
        QShortcut(QKeySequence("Ctrl+1"), self, lambda: self._switch_tab(0))
        QShortcut(QKeySequence("Ctrl+2"), self, lambda: self._switch_tab(1))
        QShortcut(QKeySequence("Ctrl+3"), self, lambda: self._switch_tab(2))
        QShortcut(QKeySequence("Ctrl+4"), self, lambda: self._switch_tab(3))
        QShortcut(QKeySequence("Ctrl+5"), self, lambda: self._switch_tab(4))
        QShortcut(QKeySequence("Ctrl+6"), self, lambda: self._switch_tab(5))
        QShortcut(QKeySequence("Ctrl+W"), self, self.close)

    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        dot = QLabel("●")
        dot.setStyleSheet(f"color: {COLORS['accent']}; font-size: 18px;")
        layout.addWidget(dot)

        title = QLabel("SD WebUI Forge")
        title.setStyleSheet(f"color:{COLORS['text_primary']};font-size:16px;font-weight:bold;margin-left:6px;")
        layout.addWidget(title)

        sub = QLabel("Neo v3")
        sub.setStyleSheet(f"color:{COLORS['accent_light']};font-size:11px;margin-left:4px;margin-top:4px;")
        layout.addWidget(sub)
        layout.addStretch()

        return header

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(160)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(2)

        self._nav_btns = []
        nav_items = [
            ("🏠", "主控台"),
            ("📄", "运行日志"),
            ("⚙️", "参数设置"),
            ("📁", "路径配置"),
            ("🧩", "插件管理"),
            ("🔍", "环境检测"),
            ("📚", "模型指南"),
            ("🧪", "插件指南"),
            ("📦", "资源汇总"),
        ]
        for i, (icon, text) in enumerate(nav_items):
            btn = QPushButton(f"  {icon}  {text}")
            btn.setCheckable(True)
            btn.setFixedHeight(44)
            btn.setStyleSheet(self._nav_btn_style())
            btn.clicked.connect(lambda checked, idx=i: self._switch_tab(idx))
            layout.addWidget(btn)
            self._nav_btns.append(btn)

        layout.addStretch()

        info = QLabel("Forge Neo v3")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(f"color:{COLORS['text_dim']};font-size:10px;")
        layout.addWidget(info)

        return sidebar

    def _nav_btn_style(self):
        return f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_secondary']};
                border: none;
                border-radius: 0;
                text-align: left;
                padding-left: 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
                color: {COLORS['text_primary']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['accent']}22;
                color: {COLORS['accent_light']};
                border-left: 4px solid {COLORS['accent']};
                border-radius: 0 8px 8px 0;
                font-weight: bold;
                padding-left: 16px;
            }}
        """

    def _build_content(self):
        # 创建主容器，使用QTabWidget但隐藏标签栏
        self.stack = QTabWidget()
        self.stack.tabBar().hide()
        self.stack.setStyleSheet(f"""
            QTabWidget::pane {{ border:none; background-color:{COLORS['bg_card']}; }}
        """)

        # 创建各个标签页
        self.tab_launch     = LaunchTab(self.config, self)
        self.tab_settings   = SettingsTab(self.config, self)
        self.tab_paths      = PathsTab(self.config, self)
        self.tab_extensions = ExtensionsTab(self.config, self)
        self.tab_env        = EnvTab(self)
        self.tab_log        = LogTab(self)
        self.tab_model_guide = ModelGuideTab(self)
        self.tab_plugin_guide = PluginGuideTab(self)
        self.tab_resource_summary = ResourceSummaryTab(self)
        
        # 创建网络代理和版本管理（作为子组件嵌入参数设置）
        self.tab_proxy      = ProxyTab(self.config, self)
        self.tab_versions   = VersionsTab(self)

        # 添加到stack
        self.stack.addTab(self.tab_launch,     "主控台")
        self.stack.addTab(self.tab_log,        "运行日志")
        self.stack.addTab(self.tab_settings,   "参数设置")
        self.stack.addTab(self.tab_paths,      "路径配置")
        self.stack.addTab(self.tab_extensions, "插件管理")
        self.stack.addTab(self.tab_env,        "环境检测")
        self.stack.addTab(self.tab_model_guide, "模型指南")
        self.stack.addTab(self.tab_plugin_guide, "插件指南")
        self.stack.addTab(self.tab_resource_summary, "资源汇总")

        # 信号连接
        self.tab_launch.sig_launch.connect(self._on_launch)
        self.tab_launch.sig_stop.connect(self._on_stop)
        self.tab_launch.sig_stop_all.connect(self._on_stop_all_confirm)
        self.tab_launch.sig_open_browser.connect(self._on_open_browser)
        self.tab_launch.sig_goto.connect(self._switch_tab)
        
        # 日志标签页信号连接
        self.tab_log.sig_stop.connect(self._on_stop)
        self.tab_log.sig_restart.connect(self._on_restart)

        # 将网络代理和版本管理嵌入到参数设置页面
        self._integrate_proxy_and_versions_into_settings()

        return self.stack

    def _integrate_proxy_and_versions_into_settings(self):
        """将网络代理和版本管理集成到参数设置页面中"""
        # 在SettingsTab中添加子标签页或区域
        if hasattr(self.tab_settings, 'add_sub_tabs'):
            # 如果SettingsTab支持添加子标签
            self.tab_settings.add_sub_tabs([
                ("基本设置", self.tab_settings),
                ("网络代理", self.tab_proxy),
                ("版本管理", self.tab_versions),
            ])
        else:
            # 否则在SettingsTab底部添加两个区域
            self.tab_settings.add_proxy_section(self.tab_proxy)
            self.tab_settings.add_versions_section(self.tab_versions)

    def _build_statusbar(self):
        bar = QFrame()
        bar.setFixedHeight(32)
        bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-top: 1px solid {COLORS['border']};
            }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)

        self.lbl_status = QLabel("● 未运行")
        self.lbl_status.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        layout.addWidget(self.lbl_status)

        self.lbl_port = QLabel(f"端口: {self.config.get('port', 7869)}")
        self.lbl_port.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        layout.addWidget(self.lbl_port)

        layout.addStretch()

        return bar

    def _build_hw_bar(self):
        self.hw_bar = HWMonitorBar()
        return self.hw_bar

    def _switch_tab(self, index: int):
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
            for i, btn in enumerate(self._nav_btns):
                btn.setChecked(i == index)

    def _on_launch(self):
        # 防止重复启动：如果已有进程在运行，先提示用户
        if self.worker and self.worker.isRunning():
            self.tab_log.append_line("⚠️  WebUI 已在运行中，请勿重复启动")
            return
        
        self.tab_settings.apply_to_config(self.config)
        self.tab_paths.apply_to_config(self.config)
        save_config(self.config)

        # 启动前检测端口
        from core.config import is_port_in_use, find_available_port
        from core.launcher import kill_process_on_port
        
        original_port = self.config.get("port", 7869)
        if is_port_in_use(original_port):
            # 尝试清理占用端口的进程
            self.tab_log.append_line(f"⚠️  检测到端口 {original_port} 被占用")
            if kill_process_on_port(original_port):
                self.tab_log.append_line(f"✅ 已清理端口 {original_port} 的占用进程")
                import time
                time.sleep(0.5)  # 等待端口释放
            else:
                # 如果清理失败，自动切换到新端口
                new_port = find_available_port(original_port)
                self.config["port"] = new_port
                save_config(self.config)
                self.tab_log.append_line(f"⚠️  无法清理端口，自动切换到端口 {new_port}")

        self.lbl_port.setText(f"端口: {self.config.get('port', 7869)}")

        self.worker = LaunchWorker(self.config)
        # 将日志输出到LogTab
        if hasattr(self, 'tab_log'):
            self.worker.log_line.connect(self.tab_log.append_line)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

        self.tab_launch.set_running(True)
        if hasattr(self, 'tab_log'):
            self.tab_log.set_running(True, 1)
        if hasattr(self, 'hw_bar'):
            self.hw_bar.set_proc_count(1)
        self.lbl_status.setText("● 运行中")
        self.lbl_status.setStyleSheet(f"color:{COLORS['green']};font-weight:bold;font-size:11px;")

        # 保持在主控台（现在包含日志）
        self._switch_tab(0)

    def _on_stop(self):
        if self.worker:
            try:
                self.worker.log_line.disconnect()
                self.worker.finished.disconnect()
            except Exception:
                pass
            self.worker.stop()
            if not self.worker.wait(3000):
                try:
                    self.worker.force_kill()
                except Exception:
                    pass
                self.worker.wait(1000)
            try:
                self.worker.deleteLater()
            except Exception:
                pass
            self.worker = None

        self.tab_launch.set_running(False)
        if hasattr(self, 'tab_log'):
            self.tab_log.set_running(False)
        if hasattr(self, 'hw_bar'):
            self.hw_bar.set_proc_count(0)
        self.lbl_status.setText("● 未运行")
        self.lbl_status.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")

    def _on_stop_all(self):
        """停止所有相关进程"""
        if self.worker and self.worker.isRunning():
            self.tab_log.append_line("[停止全部进程] 正在终止 WebUI 进程...")
            self._on_stop()
        else:
            self.tab_log.append_line("[停止全部进程] 当前没有运行中的进程")

    def _on_stop_all_confirm(self):
        # sig_stop_all is already emitted after user confirmed in tab_launch._confirm_stop_all
        # Just execute the stop action
        self._on_stop_all()

    def _on_open_browser(self):
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        port = self.config.get("port", 7869)
        url = f"http://127.0.0.1:{port}"
        QDesktopServices.openUrl(QUrl(url))

    def _on_restart(self):
        """重新启动 WebUI 进程"""
        from .theme import COLORS
        self.tab_log.append_line("[重新启动] 开始重新启动 WebUI 进程...")
        
        # 1. 先停止当前运行的进程
        if self.worker and self.worker.isRunning():
            self.tab_log.append_line("[重新启动] 正在停止当前进程...")
            try:
                self.worker.log_line.disconnect()
                self.worker.finished.disconnect()
            except Exception:
                pass
            self.worker.stop()
            if not self.worker.wait(3000):
                try:
                    self.worker.force_kill()
                except Exception:
                    pass
                self.worker.wait(1000)
            try:
                self.worker.deleteLater()
            except Exception:
                pass
            self.worker = None
            
            self.tab_launch.set_running(False)
            if hasattr(self, 'tab_log'):
                self.tab_log.set_running(False)
            if hasattr(self, 'hw_bar'):
                self.hw_bar.set_proc_count(0)
            self.lbl_status.setText("● 未运行")
            self.lbl_status.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
            
            # 等待端口释放
            import time
            time.sleep(1)
        
        # 2. 启动新的进程
        self.tab_log.append_line("[重新启动] 正在启动新进程...")
        self._on_launch()

    def _on_finished(self, code: int):
        self.tab_launch.set_running(False)
        if hasattr(self, 'tab_log'):
            self.tab_log.set_running(False)
        if hasattr(self, 'hw_bar'):
            self.hw_bar.set_proc_count(0)
        self.lbl_status.setText("● 未运行")
        self.lbl_status.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        # 在LaunchTab的日志中显示退出信息
        self.tab_launch.append_log(f"\n[进程结束] 退出码: {code}")
        if hasattr(self, 'tab_log'):
            self.tab_log.append_line(f"\n[进程结束] 退出码: {code}")
        if self.worker:
            self.worker.deleteLater()
            self.worker = None

    def closeEvent(self, event):
        save_config(self.config)
        
        # 清理所有残留的临时bat文件
        from core.launcher import cleanup_all_temp_files
        cleanup_all_temp_files()
        
        # 清理 tab_launch 的后台线程
        if hasattr(self.tab_launch, 'stop_all'):
            # 异步清理，避免阻塞退出
            import threading
            def cleanup_thread():
                try:
                    self.tab_launch.stop_all()
                except Exception:
                    pass
            threading.Thread(target=cleanup_thread, daemon=True).start()
        
        # 停止 WebUI 进程（非阻塞方式）
        if self.worker and self.worker.isRunning():
            try:
                self.worker.log_line.disconnect()
                self.worker.finished.disconnect()
            except Exception:
                pass
            
            # 异步停止进程，避免阻塞退出
            import threading
            def stop_thread():
                try:
                    self.worker.stop()
                    # 不等待进程完全停止，让它在后台自行清理
                    self.worker.deleteLater()
                except Exception:
                    pass
            threading.Thread(target=stop_thread, daemon=True).start()
        
        # 立即接受退出事件，避免卡顿
        event.accept()
