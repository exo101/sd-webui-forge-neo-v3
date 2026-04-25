"""网络代理设置 Tab"""
import os
import winreg
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QLineEdit, QComboBox,
    QCheckBox, QGroupBox, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt
from .theme import COLORS
from core.config import save_config


class ProxyTab(QWidget):
    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.config = config
        self._build_ui()
        self._load_config()

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

        # 标题
        lbl_title = QLabel("🌐  网络代理设置")
        lbl_title.setStyleSheet(f"color:{COLORS['text_primary']};font-size:18px;font-weight:bold;")
        layout.addWidget(lbl_title)

        lbl_sub = QLabel("配置全局网络代理设置，代理设置可以应用于不同的场景。")
        lbl_sub.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        layout.addWidget(lbl_sub)

        self.lbl_warn = QLabel("请确保你的代理地址正确且有效")
        self.lbl_warn.setStyleSheet(f"color:{COLORS['yellow']};font-size:11px;")
        layout.addWidget(self.lbl_warn)

        # 代理配置组
        layout.addWidget(self._build_proxy_group())

        # 影响范围组
        layout.addWidget(self._build_scope_group())

        # 保存按钮
        btn_save = QPushButton("💾  保存代理设置")
        btn_save.setFixedHeight(40)
        btn_save.setStyleSheet(f"""
            QPushButton{{background:{COLORS['accent']};color:white;border:none;
                border-radius:8px;font-size:13px;font-weight:bold;}}
            QPushButton:hover{{background:{COLORS['accent_light']};}}
        """)
        btn_save.clicked.connect(self._save)
        layout.addWidget(btn_save)

        layout.addStretch()
        scroll.setWidget(content)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    def _build_proxy_group(self) -> QGroupBox:
        g = QGroupBox("代理配置")
        g.setStyleSheet(self._group_style())
        layout = QVBoxLayout(g)
        layout.setSpacing(12)

        # 代理模式
        row1 = QHBoxLayout()
        lbl = QLabel("代理模式:")
        lbl.setFixedWidth(90)
        lbl.setStyleSheet(f"color:{COLORS['text_secondary']};")
        row1.addWidget(lbl)

        self.combo_mode = QComboBox()
        self.combo_mode.addItem("不使用代理",   "none")
        self.combo_mode.addItem("使用系统代理", "system")
        self.combo_mode.addItem("自定义代理",   "custom")
        self.combo_mode.setFixedWidth(180)
        self.combo_mode.setStyleSheet(self._input_style())
        self.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        row1.addWidget(self.combo_mode)

        self.btn_read_sys = QPushButton("读取系统代理")
        self.btn_read_sys.setFixedHeight(32)
        self.btn_read_sys.setStyleSheet(self._small_btn_style())
        self.btn_read_sys.clicked.connect(self._read_system_proxy)
        row1.addWidget(self.btn_read_sys)
        row1.addStretch()
        layout.addLayout(row1)

        # 代理地址
        row2 = QHBoxLayout()
        lbl2 = QLabel("代理地址:")
        lbl2.setFixedWidth(90)
        lbl2.setStyleSheet(f"color:{COLORS['text_secondary']};")
        row2.addWidget(lbl2)

        self.edit_proxy = QLineEdit()
        self.edit_proxy.setPlaceholderText("http://127.0.0.1:7890")
        self.edit_proxy.setStyleSheet(self._input_style())
        row2.addWidget(self.edit_proxy, 1)
        layout.addLayout(row2)

        # 当前状态
        self.lbl_status = QLabel("当前状态: 不使用代理")
        self.lbl_status.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        layout.addWidget(self.lbl_status)

        return g

    def _build_scope_group(self) -> QGroupBox:
        g = QGroupBox("影响范围")
        g.setStyleSheet(self._group_style())
        layout = QVBoxLayout(g)
        layout.setSpacing(8)

        scopes = [
            ("proxy_scope_launcher", "启动器自身（检查更新、下载依赖等）"),
            ("proxy_scope_webui",    "常规启动/不更新启动（Python 进程的网络请求）"),
            ("proxy_scope_git",      "命令行工具（Git、pip 等）"),
        ]
        self._scope_checks = {}
        for key, text in scopes:
            chk = QCheckBox(text)
            chk.setStyleSheet(f"color:{COLORS['text_primary']};font-size:13px;")
            layout.addWidget(chk)
            self._scope_checks[key] = chk

        return g

    # ── 逻辑 ──────────────────────────────────────────────────

    def _on_mode_changed(self, idx: int):
        mode = self.combo_mode.currentData()
        self.edit_proxy.setEnabled(mode == "custom")
        self.btn_read_sys.setEnabled(mode == "system")

        if mode == "none":
            self.lbl_status.setText("当前状态: 不使用代理")
            self.lbl_warn.hide()
        elif mode == "system":
            self.lbl_status.setText("当前状态: 使用系统代理")
            self.lbl_warn.show()
        else:
            addr = self.edit_proxy.text().strip() or "未填写"
            self.lbl_status.setText(f"当前状态: 自定义代理 {addr}")
            self.lbl_warn.show()

    def _read_system_proxy(self):
        """从 Windows 注册表读取系统代理"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
            enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if enabled:
                server, _ = winreg.QueryValueEx(key, "ProxyServer")
                if not server.startswith("http"):
                    server = "http://" + server
                self.edit_proxy.setText(server)
                self.lbl_status.setText(f"已读取系统代理: {server}")
            else:
                self.lbl_status.setText("系统代理未启用")
            winreg.CloseKey(key)
        except Exception as e:
            self.lbl_status.setText(f"读取失败: {e}")

    def _load_config(self):
        proxy_cfg = self.config.get("proxy", {})
        mode = proxy_cfg.get("mode", "none")
        idx = self.combo_mode.findData(mode)
        self.combo_mode.setCurrentIndex(max(0, idx))
        self.edit_proxy.setText(proxy_cfg.get("address", ""))
        for key, chk in self._scope_checks.items():
            chk.setChecked(proxy_cfg.get(key, False))
        self._on_mode_changed(self.combo_mode.currentIndex())

    def _save(self):
        mode = self.combo_mode.currentData()
        addr = self.edit_proxy.text().strip()

        # 验证代理地址格式
        if mode == "custom" and addr:
            if not (addr.startswith("http://") or addr.startswith("https://")):
                QMessageBox.warning(self, "格式错误",
                    "代理地址必须以 http:// 或 https:// 开头\n例如: http://127.0.0.1:7890")
                return
            try:
                from urllib.parse import urlparse
                r = urlparse(addr)
                if not r.netloc:
                    raise ValueError
            except Exception:
                QMessageBox.warning(self, "格式错误", "代理地址格式不正确")
                return

        self.config["proxy"] = {"mode": mode, "address": addr}
        for key, chk in self._scope_checks.items():
            self.config["proxy"][key] = chk.isChecked()

        save_config(self.config)
        self.lbl_status.setText(f"✅ 已保存 · {self.combo_mode.currentText()}"
                                + (f" · {addr}" if addr else ""))
        self.lbl_status.setStyleSheet(f"color:{COLORS['green']};font-size:11px;")

    def get_effective_proxy(self) -> str:
        """返回当前生效的代理地址字符串，供其他模块使用"""
        proxy_cfg = self.config.get("proxy", {})
        mode = proxy_cfg.get("mode", "none")
        if mode == "none":
            return ""
        if mode == "custom":
            return proxy_cfg.get("address", "")
        if mode == "system":
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
                enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
                if enabled:
                    server, _ = winreg.QueryValueEx(key, "ProxyServer")
                    winreg.CloseKey(key)
                    return "http://" + server if not server.startswith("http") else server
            except Exception:
                pass
        return ""

    # ── 样式 ──────────────────────────────────────────────────

    def _group_style(self) -> str:
        return f"""
            QGroupBox{{color:{COLORS['accent_light']};border:1px solid {COLORS['border']};
                border-radius:8px;margin-top:12px;padding-top:8px;font-weight:bold;}}
            QGroupBox::title{{subcontrol-origin:margin;left:12px;padding:0 6px;}}
        """

    def _input_style(self) -> str:
        return f"""
            QLineEdit,QComboBox{{background:{COLORS['bg_input']};color:{COLORS['text_primary']};
                border:1px solid {COLORS['border']};border-radius:5px;
                padding:5px 10px;font-size:12px;}}
            QLineEdit:focus,QComboBox:focus{{border-color:{COLORS['border_focus']};}}
            QComboBox::drop-down{{border:none;width:20px;}}
            QComboBox QAbstractItemView{{background:{COLORS['bg_input']};
                color:{COLORS['text_primary']};border:1px solid {COLORS['border_focus']};
                selection-background-color:{COLORS['accent']};}}
        """

    def _small_btn_style(self) -> str:
        return f"""
            QPushButton{{background:{COLORS['bg_hover']};color:{COLORS['text_secondary']};
                border:1px solid {COLORS['border']};border-radius:5px;
                padding:4px 12px;font-size:12px;}}
            QPushButton:hover{{background:{COLORS['accent']}33;color:{COLORS['text_primary']};}}
            QPushButton:disabled{{color:{COLORS['text_dim']};}}
        """
