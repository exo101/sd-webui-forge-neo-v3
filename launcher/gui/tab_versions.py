"""版本管理标签页"""
from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem,
    QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from core.version_manager import (
    load_versions, get_current_version, set_current_version,
    check_github_update, update_from_github, refresh_local_versions
)


class UpdateCheckThread(QThread):
    """后台检查更新的线程"""
    finished = pyqtSignal(dict)  # 发送检查结果
    
    def run(self):
        result = check_github_update()
        self.finished.emit(result or {})


class UpdateThread(QThread):
    """后台执行更新的线程"""
    progress = pyqtSignal(str)  # 进度消息
    finished = pyqtSignal(bool, str)  # (成功与否, 消息)
    
    def run(self):
        def callback(msg):
            self.progress.emit(msg)
        
        success, message = update_from_github(progress_callback=callback)
        self.finished.emit(success, message)


class VersionsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_window = parent
        self._update_check_thread = None
        self._update_thread = None
        self._init_ui()
        self.refresh_versions()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Title row with Refresh and Update buttons
        title_row = QHBoxLayout()
        title = QLabel("版本管理")
        title.setStyleSheet("font-size:14px; font-weight:600;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        # GitHub更新按钮
        self.btn_check_update = QPushButton("🔄 检查GitHub更新")
        self.btn_check_update.setStyleSheet(
            "background-color:#2a7bd5; color:white; padding:6px 12px; border-radius:4px;"
        )
        self.btn_check_update.clicked.connect(self.check_for_updates)
        title_row.addWidget(self.btn_check_update)
        
        # 刷新版本列表按钮
        self.btn_refresh = QPushButton("刷新版本列表")
        self.btn_refresh.setStyleSheet("background-color:#2e7d32; color:white; padding:6px 12px; border-radius:4px;")
        self.btn_refresh.clicked.connect(self.refresh_versions)
        title_row.addWidget(self.btn_refresh)
        layout.addLayout(title_row)

        # Current version info
        self.lbl_current = QLabel()
        self.lbl_current.setWordWrap(True)
        self.lbl_current.setStyleSheet("font-size:12px; color:#99d2a6;")
        layout.addWidget(self.lbl_current)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(divider)

        # Versions list
        self.list_versions = QListWidget()
        layout.addWidget(self.list_versions)

        # Spacer to push content up
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def check_for_updates(self):
        """检查GitHub更新"""
        self.btn_check_update.setEnabled(False)
        self.btn_check_update.setText("⏳ 检查中...")
        
        # 创建后台线程
        self._update_check_thread = UpdateCheckThread()
        self._update_check_thread.finished.connect(self.on_update_check_finished)
        self._update_check_thread.start()
    
    def on_update_check_finished(self, result):
        """更新检查完成回调"""
        self.btn_check_update.setEnabled(True)
        self.btn_check_update.setText("🔄 检查GitHub更新")
        
        if not result:
            QMessageBox.warning(self, "检查失败", "无法连接到GitHub，请检查网络连接")
            return
        
        if not result.get('has_update'):
            QMessageBox.information(
                self, 
                "无需更新", 
                f"当前已是最新版本\n版本: {result.get('current_version', '未知')}"
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
            f"是否立即更新？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.perform_update()
    
    def perform_update(self):
        """执行更新"""
        # 禁用按钮
        self.btn_check_update.setEnabled(False)
        self.btn_refresh.setEnabled(False)
        
        # 创建进度对话框
        self.progress_dialog = QProgressDialog("正在更新...", "取消", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setWindowTitle("更新启动器")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.show()
        
        # 创建更新线程
        self._update_thread = UpdateThread()
        self._update_thread.progress.connect(self.on_update_progress)
        self._update_thread.finished.connect(self.on_update_finished)
        self._update_thread.start()
    
    def on_update_progress(self, message):
        """更新进度回调"""
        self.progress_dialog.setLabelText(message)
    
    def on_update_finished(self, success, message):
        """更新完成回调"""
        self.progress_dialog.close()
        self.btn_check_update.setEnabled(True)
        self.btn_refresh.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "更新成功", message)
            # 刷新版本列表
            self.refresh_versions()
        else:
            QMessageBox.critical(self, "更新失败", message)

    def refresh_versions(self):
        # 先从Git刷新本地版本列表
        versions = refresh_local_versions()
        
        data = load_versions()
        current = data.get('current_version', 'v1.0.0')
        self.lbl_current.setText(f"当前版本: {current}")

        self.list_versions.clear()
        if not versions:
            item = QListWidgetItem("无可用版本，请检查版本源或手动添加版本")
            self.list_versions.addItem(item)
            return

        for v in versions:
            vid = v.get('id', 'unknown')
            date = v.get('date', '')
            msg = v.get('message', '')
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(6, 6, 6, 6)
            item_layout.setSpacing(10)

            v_label = QLabel(f"{vid}  {date}\n{msg}")
            v_label.setStyleSheet("font-size:12px;")
            v_label.setWordWrap(True)
            item_layout.addWidget(v_label)
            item_layout.addStretch()

            btn = QPushButton("切换到此版本")
            btn.setStyleSheet("background-color:#2a7bd5; color:white; padding:6px 12px; border-radius:4px;")
            btn.clicked.connect(lambda checked, v_id=vid: self._switch_version(v_id))
            item_layout.addWidget(btn)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.list_versions.addItem(list_item)
            self.list_versions.setItemWidget(list_item, item_widget)

    def _switch_version(self, version_id: str):
        # 这里执行最小层面的切换：更新版本记录，并在界面上刷新当前版本信息
        set_current_version(version_id)
        # 刷新当前版本信息展示
        self.refresh_versions()
        # 让父窗口的状态栏也显示版本切换提示（若需要可扩展）
        if self._main_window:
            try:
                self._main_window.lbl_version.setText(f"版本: {version_id}")
            except Exception:
                pass
