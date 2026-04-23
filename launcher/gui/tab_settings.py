"""参数设置 Tab"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QSpinBox, QComboBox, QLineEdit,
    QGroupBox, QScrollArea, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from .theme import COLORS


class SettingsTab(QWidget):
    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.config = config
        self._widgets = {}
        self._build_ui()
        self._load_config()

    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['bg_card']};")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # 服务设置
        layout.addWidget(self._group_service())
        # CUDA 优化
        layout.addWidget(self._group_cuda())
        # 注意力机制
        layout.addWidget(self._group_attention())
        # 显存优化
        layout.addWidget(self._group_vram())
        # 精度设置
        layout.addWidget(self._group_precision())
        # 其他
        layout.addWidget(self._group_misc())
        # 额外参数
        layout.addWidget(self._group_extra())
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['border']};")
        separator.setFixedHeight(2)
        layout.addWidget(separator)
        
        # 网络代理区域（占位，将在main_window中注入实际内容）
        self.proxy_container = QWidget()
        self.proxy_layout = QVBoxLayout(self.proxy_container)
        self.proxy_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.proxy_container)
        
        # 版本管理区域（占位，将在main_window中注入实际内容）
        self.versions_container = QWidget()
        self.versions_layout = QVBoxLayout(self.versions_container)
        self.versions_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.versions_container)
        
        layout.addStretch()

        scroll.setWidget(content)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    def _group_service(self) -> QGroupBox:
        g = QGroupBox("服务设置")
        layout = QGridLayout(g)
        layout.setSpacing(12)

        layout.addWidget(QLabel("端口:"), 0, 0)
        spin = QSpinBox()
        spin.setRange(1024, 65535)
        spin.setFixedWidth(100)
        layout.addWidget(spin, 0, 1)
        self._widgets["port"] = spin

        layout.addWidget(QLabel("主题:"), 0, 2)
        combo = QComboBox()
        combo.addItems(["dark", "light"])
        combo.setFixedWidth(100)
        layout.addWidget(combo, 0, 3)
        self._widgets["theme"] = combo

        chk_listen = QCheckBox("监听所有IP (--listen)")
        chk_autolaunch = QCheckBox("自动打开浏览器 (--autolaunch)")
        chk_api = QCheckBox("启用 API (--api)")
        chk_share = QCheckBox("Gradio 分享 (--share)")
        layout.addWidget(chk_listen, 1, 0, 1, 2)
        layout.addWidget(chk_autolaunch, 1, 2, 1, 2)
        layout.addWidget(chk_api, 2, 0, 1, 2)
        layout.addWidget(chk_share, 2, 2, 1, 2)
        self._widgets["listen"] = chk_listen
        self._widgets["autolaunch"] = chk_autolaunch
        self._widgets["api"] = chk_api
        self._widgets["share"] = chk_share

        return g

    def _group_cuda(self) -> QGroupBox:
        g = QGroupBox("CUDA 优化")
        layout = QHBoxLayout(g)
        layout.setSpacing(20)

        for key, text in [
            ("cuda_malloc",       "--cuda-malloc"),
            ("cuda_stream",       "--cuda-stream"),
            ("pin_shared_memory", "--pin-shared-memory"),
        ]:
            chk = QCheckBox(text)
            layout.addWidget(chk)
            self._widgets[key] = chk
        layout.addStretch()
        return g

    def _group_attention(self) -> QGroupBox:
        g = QGroupBox("注意力机制")
        layout = QHBoxLayout(g)
        layout.setSpacing(20)

        for key, text in [
            ("disable_sage",     "--disable-sage"),
            ("disable_flash",    "--disable-flash"),
            ("disable_xformers", "--disable-xformers"),
            ("xformers",         "--xformers"),
        ]:
            chk = QCheckBox(text)
            layout.addWidget(chk)
            self._widgets[key] = chk
        layout.addStretch()
        return g

    def _group_vram(self) -> QGroupBox:
        g = QGroupBox("显存优化")
        layout = QHBoxLayout(g)
        layout.setSpacing(20)

        lbl = QLabel("显存模式:")
        lbl.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(lbl)

        for key, text in [
            ("medvram", "--medvram (中等显存)"),
            ("lowvram",  "--lowvram (低显存)"),
        ]:
            chk = QCheckBox(text)
            layout.addWidget(chk)
            self._widgets[key] = chk
        layout.addStretch()
        return g

    def _group_precision(self) -> QGroupBox:
        g = QGroupBox("精度设置")
        layout = QHBoxLayout(g)
        layout.setSpacing(20)

        for key, text in [
            ("no_half",       "--no-half"),
            ("no_half_vae",   "--no-half-vae"),
            ("precision_full","--precision full"),
        ]:
            chk = QCheckBox(text)
            layout.addWidget(chk)
            self._widgets[key] = chk
        layout.addStretch()
        return g

    def _group_misc(self) -> QGroupBox:
        g = QGroupBox("其他选项")
        layout = QHBoxLayout(g)
        layout.setSpacing(20)

        for key, text in [
            ("skip_install",   "--skip-install"),
            ("skip_version",   "--skip-version-check"),
            ("skip_torch",     "--skip-torch-cuda-test"),
        ]:
            chk = QCheckBox(text)
            layout.addWidget(chk)
            self._widgets[key] = chk
        layout.addStretch()
        return g

    def _group_extra(self) -> QGroupBox:
        g = QGroupBox("额外命令行参数")
        layout = QVBoxLayout(g)

        lbl = QLabel("在此输入额外的启动参数，多个参数用空格分隔：")
        lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        layout.addWidget(lbl)

        edit = QLineEdit()
        edit.setPlaceholderText("例如: --no-gradio-queue --gradio-auth user:pass")
        layout.addWidget(edit)
        self._widgets["extra_args"] = edit
        return g

    def _load_config(self):
        c = self.config
        self._widgets["port"].setValue(c.get("port", 7869))
        idx = self._widgets["theme"].findText(c.get("theme", "dark"))
        self._widgets["theme"].setCurrentIndex(max(0, idx))

        for key in ["listen", "autolaunch", "api", "share",
                    "cuda_malloc", "cuda_stream", "pin_shared_memory",
                    "disable_sage", "disable_flash", "disable_xformers", "xformers",
                    "medvram", "lowvram", "no_half", "no_half_vae", "precision_full",
                    "skip_install", "skip_version", "skip_torch"]:
            if key in self._widgets:
                self._widgets[key].setChecked(bool(c.get(key, False)))

        self._widgets["extra_args"].setText(c.get("extra_args", ""))

    def apply_to_config(self, config: dict):
        config["port"]  = self._widgets["port"].value()
        config["theme"] = self._widgets["theme"].currentText()

        for key in ["listen", "autolaunch", "api", "share",
                    "cuda_malloc", "cuda_stream", "pin_shared_memory",
                    "disable_sage", "disable_flash", "disable_xformers", "xformers",
                    "medvram", "lowvram", "no_half", "no_half_vae", "precision_full",
                    "skip_install", "skip_version", "skip_torch"]:
            if key in self._widgets:
                config[key] = self._widgets[key].isChecked()

        config["extra_args"] = self._widgets["extra_args"].text().strip()

    def add_proxy_section(self, proxy_tab_widget):
        """在参数设置中添加网络代理区域"""
        # 添加标题
        title_label = QLabel("🌐 网络代理设置")
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold; margin-top: 8px;")
        self.proxy_layout.addWidget(title_label)
        
        # 将ProxyTab的内容移动到这里
        if hasattr(proxy_tab_widget, 'layout') and proxy_tab_widget.layout():
            # 获取ProxyTab的所有子widget并移动到proxy_container
            proxy_layout = proxy_tab_widget.layout()
            for i in range(proxy_layout.count()):
                item = proxy_layout.itemAt(i)
                if item is not None and item.widget():
                    self.proxy_layout.addWidget(item.widget())
    
    def add_versions_section(self, versions_tab_widget):
        """在参数设置中添加版本管理区域"""
        # 添加标题
        title_label = QLabel("🗂 版本管理")
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold; margin-top: 16px;")
        self.versions_layout.addWidget(title_label)
        
        # 将VersionsTab的内容移动到这里
        if hasattr(versions_tab_widget, 'layout') and versions_tab_widget.layout():
            # 获取VersionsTab的所有子widget并移动到versions_container
            versions_layout = versions_tab_widget.layout()
            for i in range(versions_layout.count()):
                item = versions_layout.itemAt(i)
                if item is not None and item.widget():
                    self.versions_layout.addWidget(item.widget())
