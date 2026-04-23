"""运行状态 / 日志 Tab"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QPlainTextEdit, QLabel, QSlider, QCheckBox, QFrame,
    QApplication, QToolTip
)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QSyntaxHighlighter
from .theme import COLORS


# ── 日志语法高亮 ──────────────────────────────────────────────

class LogHighlighter(QSyntaxHighlighter):
    """对日志内容做关键词高亮"""

    def __init__(self, document):
        super().__init__(document)
        self._rules = []

        def rule(pattern, color, bold=False):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if bold:
                fmt.setFontWeight(QFont.Weight.Bold)
            self._rules.append((pattern, fmt))

        # 错误类（红色加粗）
        for kw in ["Error", "ERROR", "Exception", "EXCEPTION",
                   "Traceback", "FAILED", "failed", "错误"]:
            rule(kw, "#ff6b6b", bold=True)

        # 警告类（橙色）
        for kw in ["Warning", "WARNING", "warn", "WARN"]:
            rule(kw, "#ffb86c")

        # 成功类（绿色）
        for kw in ["Successfully", "success", "SUCCESS", "✅", "完成", "done", "Done"]:
            rule(kw, "#50fa7b")

        # 文件路径（青色）
        rule(r"[A-Za-z]:\\[^\s]+", "#8be9fd")

        # 进度百分比（黄色）
        rule(r"\d+%", "#f1fa8c")

    def highlightBlock(self, text: str):
        import re
        for pattern, fmt in self._rules:
            for m in re.finditer(pattern, text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


class LogTab(QWidget):
    sig_stop    = pyqtSignal()
    sig_restart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._paused = False
        self._free_scroll = False
        self._font_size = 12
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 12)
        layout.setSpacing(10)

        # ── 顶部标题 + 终止/重启 + 更新内核 ──────────────────────────────
        top = QHBoxLayout()

        title_col = QVBoxLayout()
        lbl_title = QLabel("📊  程序运行状态")
        lbl_title.setStyleSheet(f"color:{COLORS['text_primary']};font-size:18px;font-weight:bold;")
        title_col.addWidget(lbl_title)
        lbl_sub = QLabel("实时查看程序启动和运行的详细信息")
        lbl_sub.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        title_col.addWidget(lbl_sub)
        top.addLayout(title_col)
        top.addStretch()

        self.btn_update = QPushButton("🆙  更新内核")
        self.btn_update.setFixedSize(110, 36)
        self.btn_update.setStyleSheet(self._btn_style("#1a1a3a", COLORS['cyan'], "#1a1a5a"))
        self.btn_update.clicked.connect(self._on_update_kernel)
        top.addWidget(self.btn_update)
        
        # 清理内存与显存按钮
        self.btn_clean_memory = QPushButton("🧹  清理内存与显存")
        self.btn_clean_memory.setFixedSize(130, 36)
        self.btn_clean_memory.setStyleSheet(self._btn_style("#2a3a2a", COLORS['green'], "#1a4a1a"))
        self.btn_clean_memory.clicked.connect(self._on_clean_memory)
        top.addWidget(self.btn_clean_memory)

        self.btn_terminate = QPushButton("■  终止程序")
        self.btn_terminate.setFixedSize(110, 36)
        self.btn_terminate.setEnabled(False)
        self.btn_terminate.setStyleSheet(self._btn_style("#3d1f1f", COLORS['red'], "#5a2020"))
        self.btn_terminate.clicked.connect(self.sig_stop.emit)
        top.addWidget(self.btn_terminate)

        self.btn_restart = QPushButton("↺  重新启动")
        self.btn_restart.setFixedSize(110, 36)
        self.btn_restart.setEnabled(False)
        self.btn_restart.setStyleSheet(self._btn_style("#1a3a1a", COLORS['green'], "#1f5a1f"))
        self.btn_restart.clicked.connect(self.sig_restart.emit)
        top.addWidget(self.btn_restart)

        layout.addLayout(top)

        # ── 日志工具栏 ────────────────────────────────────────
        toolbar = QFrame()
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-radius: 6px;
                border: 1px solid {COLORS['border']};
            }}
        """)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 6, 12, 6)
        tb_layout.setSpacing(10)

        lbl_log = QLabel("📄  运行日志")
        lbl_log.setStyleSheet(f"color:{COLORS['text_primary']};font-weight:bold;font-size:13px;")
        tb_layout.addWidget(lbl_log)
        tb_layout.addStretch()

        # 字体大小
        tb_layout.addWidget(QLabel("字体"))
        self.lbl_font_size = QLabel(str(self._font_size))
        self.lbl_font_size.setFixedWidth(24)
        self.lbl_font_size.setStyleSheet(f"color:{COLORS['accent_light']};font-weight:bold;")
        tb_layout.addWidget(self.lbl_font_size)

        font_slider = QSlider(Qt.Orientation.Horizontal)
        font_slider.setRange(8, 20)
        font_slider.setValue(self._font_size)
        font_slider.setFixedWidth(100)
        font_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{ height:4px; background:{COLORS['border']}; border-radius:2px; }}
            QSlider::handle:horizontal {{ background:{COLORS['accent']}; width:12px; height:12px; margin:-4px 0; border-radius:6px; }}
            QSlider::sub-page:horizontal {{ background:{COLORS['accent']}; border-radius:2px; }}
        """)
        font_slider.valueChanged.connect(self._on_font_size)
        tb_layout.addWidget(font_slider)

        # 分隔线
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"color:{COLORS['border']};")
        tb_layout.addWidget(sep)

        # 刷新按钮
        btn_refresh = QPushButton("↺")
        btn_refresh.setFixedSize(28, 28)
        btn_refresh.setToolTip("滚动到底部")
        btn_refresh.setStyleSheet(self._small_btn_style())
        btn_refresh.clicked.connect(self._scroll_to_bottom)
        tb_layout.addWidget(btn_refresh)

        layout.addWidget(toolbar)

        # ── 更新注意事项按钮 ────────────────────────────────────
        btn_update_notes = QPushButton("⚠️  更新注意事项")
        btn_update_notes.setFixedHeight(36)
        btn_update_notes.setStyleSheet(f"""
            QPushButton {{
                background-color: #1a3a1a;
                color: {COLORS['green']};
                border: 1px solid #50fa7b44;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1f5a1f;
            }}
        """)
        btn_update_notes.clicked.connect(self._show_update_notes)
        layout.addWidget(btn_update_notes)

        # ── 日志文本框 ────────────────────────────────────────
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self._apply_font()
        # 启用语法高亮
        self._highlighter = LogHighlighter(self.text_edit.document())
        layout.addWidget(self.text_edit, 1)

        # ── 底部工具栏 ────────────────────────────────────────
        bottom = QHBoxLayout()

        self.lbl_proc_count = QLabel("运行中的程序: 0")
        self.lbl_proc_count.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        bottom.addWidget(self.lbl_proc_count)
        bottom.addStretch()

        # 自由滚动
        self.chk_free_scroll = QCheckBox("自由滚动")
        self.chk_free_scroll.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:12px;")
        self.chk_free_scroll.toggled.connect(lambda v: setattr(self, '_free_scroll', v))
        bottom.addWidget(self.chk_free_scroll)

        # 暂停日志
        self.btn_pause = QPushButton("⏸  暂停日志")
        self.btn_pause.setFixedHeight(32)
        self.btn_pause.setStyleSheet(self._btn_style("#2a2a1a", COLORS['yellow'], "#3a3a1a"))
        self.btn_pause.clicked.connect(self._toggle_pause)
        bottom.addWidget(self.btn_pause)

        # 跳转到下一个错误
        self.btn_next_err = QPushButton("⚠  下一个错误")
        self.btn_next_err.setFixedHeight(32)
        self.btn_next_err.setStyleSheet(self._btn_style("#2a1a0a", COLORS['orange'], "#3a2a0a"))
        self.btn_next_err.setToolTip("跳转到下一处错误行")
        self.btn_next_err.clicked.connect(self._jump_next_error)
        bottom.addWidget(self.btn_next_err)

        # 复制错误
        self.btn_copy_err = QPushButton("📋  复制错误")
        self.btn_copy_err.setFixedHeight(32)
        self.btn_copy_err.setStyleSheet(self._btn_style("#1a2a3a", COLORS['cyan'], "#1a3a4a"))
        self.btn_copy_err.clicked.connect(self._copy_errors)
        bottom.addWidget(self.btn_copy_err)

        # 清空日志
        btn_clear = QPushButton("🗑  清空日志")
        btn_clear.setFixedHeight(32)
        btn_clear.setStyleSheet(self._btn_style("#3d1f1f", COLORS['red'], "#5a2020"))
        btn_clear.clicked.connect(self.clear)
        bottom.addWidget(btn_clear)

        layout.addLayout(bottom)

    # ── 公共接口 ──────────────────────────────────────────────

    def append_line(self, line: str):
        if self._paused:
            return
        self.text_edit.appendPlainText(line)
        if not self._free_scroll:
            self._scroll_to_bottom()

    def clear(self):
        self.text_edit.clear()

    def set_running(self, running: bool, count: int = 0):
        self.btn_terminate.setEnabled(running)
        self.btn_restart.setEnabled(running)
        self.lbl_proc_count.setText(f"运行中的程序: {count if running else 0}")

    # ── 内部方法 ──────────────────────────────────────────────

    def _on_font_size(self, val: int):
        self._font_size = val
        self.lbl_font_size.setText(str(val))
        self._apply_font()

    def _apply_font(self):
        self.text_edit.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['green']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-family: Consolas, "Courier New", monospace;
                font-size: {self._font_size}px;
            }}
        """)

    def _scroll_to_bottom(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    def _toggle_pause(self):
        self._paused = not self._paused
        if self._paused:
            self.btn_pause.setText("▶  继续日志")
            self.btn_pause.setStyleSheet(self._btn_style("#1a3a1a", COLORS['green'], "#1f5a1f"))
            # 暂停时边框变黄提示
            self.text_edit.setStyleSheet(f"""
                QPlainTextEdit {{
                    background-color: {COLORS['bg_dark']};
                    color: {COLORS['green']};
                    border: 2px solid {COLORS['yellow']};
                    border-radius: 6px;
                    font-family: Consolas, "Courier New", monospace;
                    font-size: {self._font_size}px;
                }}
            """)
        else:
            self.btn_pause.setText("⏸  暂停日志")
            self.btn_pause.setStyleSheet(self._btn_style("#2a2a1a", COLORS['yellow'], "#3a3a1a"))
            self._apply_font()
            self._scroll_to_bottom()

    def _copy_errors(self):
        text = self.text_edit.toPlainText()
        error_keywords = ["error", "exception", "traceback", "failed", "错误", "syntax"]
        errors = [l for l in text.splitlines()
                  if any(k in l.lower() for k in error_keywords)]

        if errors:
            content = "\n".join(errors)
            QApplication.clipboard().setText(content)
            count = len(errors)
            # 按钮短暂变绿提示复制成功
            orig_style = self.btn_copy_err.styleSheet()
            self.btn_copy_err.setText(f"✅  已复制 {count} 行")
            self.btn_copy_err.setStyleSheet(
                self._btn_style("#1a3a1a", COLORS['green'], "#1f5a1f"))
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: (
                self.btn_copy_err.setText("📋  复制错误"),
                self.btn_copy_err.setStyleSheet(orig_style)
            ))
        else:
            # 没有错误时按钮变灰提示
            orig_style = self.btn_copy_err.styleSheet()
            self.btn_copy_err.setText("🔍  未找到错误")
            self.btn_copy_err.setStyleSheet(
                self._btn_style(COLORS['bg_card'], COLORS['text_dim'], COLORS['bg_hover']))
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: (
                self.btn_copy_err.setText("📋  复制错误"),
                self.btn_copy_err.setStyleSheet(orig_style)
            ))

    def _jump_next_error(self):
        """从当前光标位置向下找下一个错误行并跳转高亮"""
        error_keywords = ["error", "exception", "traceback", "failed", "错误", "syntax"]
        doc = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        start_block = cursor.blockNumber()
        total = doc.blockCount()

        # 从当前行的下一行开始搜索，循环一圈
        for offset in range(1, total + 1):
            block_num = (start_block + offset) % total
            block = doc.findBlockByNumber(block_num)
            line = block.text().lower()
            if any(k in line for k in error_keywords):
                # 跳转到该行
                new_cursor = QTextCursor(block)
                new_cursor.select(QTextCursor.SelectionType.LineUnderCursor)
                self.text_edit.setTextCursor(new_cursor)
                self.text_edit.ensureCursorVisible()

                # 按钮短暂提示
                self.btn_next_err.setText("⚠  已定位")
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(1000, lambda: self.btn_next_err.setText("⚠  下一个错误"))
                return

        # 没找到
        self.btn_next_err.setText("✅  无错误")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1500, lambda: self.btn_next_err.setText("⚠  下一个错误"))

    def _btn_style(self, bg, fg, hover):
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {fg}44;
                border-radius: 5px;
                padding: 4px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
            QPushButton:disabled {{ background-color: {COLORS['bg_card']}; color: {COLORS['text_dim']}; border-color: {COLORS['border']}; }}
        """

    def _show_update_notes(self):
        """显示更新注意事项"""
        from PyQt6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("更新注意事项")
        msg.setText("在更新内核之前，请记得备份以下内置插件：")
        msg.setInformativeText(
            "内置插件目录：sd-webui-forge-neo-v3\\webui\\extensions-builtin\n\n"+
            "- 显存防溢出保护 (sd_forge_neveroom)\n"+
            "- 图像拼接参考 (sd_forge_image_stitch)\n"+
            "- 频谱预测加速 (sd_forge_spectrum)\n"+
            "- 径向注意力 (sd_forge_radial)\n"+
            "- PyTorch 编译加速 (sd_forge_compile)\n"+
            "- 多扩散 (sd_forge_multidiffusion)\n\n"+
            "原作者的更新会覆盖汉化内容。"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.exec()


    
    def _on_clean_memory(self):
        """清理内存与显存按钮点击事件"""
        from PyQt6.QtWidgets import QMessageBox
        import gc
        
        # 显示确认信息
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("清理内存与显存")
        msg.setText("确定要清理内存与显存吗？")
        msg.setInformativeText("这将尝试释放 Python 进程的内存和显存。")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        
        if msg.exec() == QMessageBox.StandardButton.Ok:
            self.append_line("[清理内存与显存] 开始清理内存与显存...")
            
            try:
                # 尝试导入 torch 以清理显存
                try:
                    import torch
                    if torch.cuda.is_available():
                        self.append_line("[清理内存与显存] 清理 CUDA 缓存...")
                        torch.cuda.empty_cache()
                        torch.cuda.ipc_collect()
                        self.append_line("[清理内存与显存] CUDA 缓存清理完成")
                    else:
                        self.append_line("[清理内存与显存] CUDA 不可用，跳过显存清理")
                except ImportError:
                    self.append_line("[清理内存与显存] PyTorch 未安装，跳过显存清理")
                
                # 强制垃圾回收
                self.append_line("[清理内存与显存] 执行垃圾回收...")
                gc.collect()
                self.append_line("[清理内存与显存] 垃圾回收完成")
                
                self.append_line("[清理内存与显存] 内存与显存清理完成")
            except Exception as e:
                self.append_line(f"[清理内存与显存] 执行清理命令时出错：{str(e)}")

    def _on_update_kernel(self):
        """更新内核按钮点击事件"""
        from PyQt6.QtWidgets import QMessageBox
        import subprocess
        import os
        
        # 显示提示信息，提醒用户备份内置插件
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("更新内核")
        msg.setText("在更新内核之前，请记得备份以下内置插件：")
        msg.setInformativeText(
            "内置插件目录：sd-webui-forge-neo-v3\\webui\\extensions-builtin\n\n"+
            "- 显存防溢出保护 (sd_forge_neveroom)\n"+
            "- 图像拼接参考 (sd_forge_image_stitch)\n"+
            "- 频谱预测加速 (sd_forge_spectrum)\n"+
            "- 径向注意力 (sd_forge_radial)\n"+
            "- PyTorch 编译加速 (sd_forge_compile)\n"+
            "- 多扩散 (sd_forge_multidiffusion)\n\n"+
            "原作者的更新会覆盖汉化内容。"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        
        # 执行更新操作
        if msg.exec() == QMessageBox.StandardButton.Ok:
            self.append_line("[更新内核] 开始更新 ForgeNeo...")
            
            # 参考 0.升级ForgeNeo.bat 的方法，直接执行 git 命令
            try:
                webui_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "webui")
                if os.path.exists(webui_dir):
                    # 执行 git pull
                    self.append_line("[更新内核] 执行 git pull...")
                    result = subprocess.run(
                        ["git", "-C", webui_dir, "pull"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            self.append_line(f"[更新内核] {line.strip()}")
                    
                    # 如果 git pull 失败，执行 git reset --hard 然后再次 pull
                    if result.returncode != 0:
                        self.append_line("[更新内核] git pull 失败，尝试 git reset --hard...")
                        
                        # 执行 git reset --hard
                        reset_result = subprocess.run(
                            ["git", "-C", webui_dir, "reset", "--hard"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True
                        )
                        
                        for line in reset_result.stdout.split('\n'):
                            if line.strip():
                                self.append_line(f"[更新内核] {line.strip()}")
                        
                        # 再次执行 git pull
                        if reset_result.returncode == 0:
                            self.append_line("[更新内核] 再次执行 git pull...")
                            
                            pull_result = subprocess.run(
                                ["git", "-C", webui_dir, "pull"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True
                            )
                            
                            for line in pull_result.stdout.split('\n'):
                                if line.strip():
                                    self.append_line(f"[更新内核] {line.strip()}")
                            
                            if pull_result.returncode == 0:
                                self.append_line("[更新内核] 更新完成，请重启应用程序。")
                            else:
                                self.append_line(f"[更新内核] 更新失败，返回代码：{pull_result.returncode}")
                        else:
                            self.append_line(f"[更新内核] git reset --hard 失败，返回代码：{reset_result.returncode}")
                    else:
                        self.append_line("[更新内核] 更新完成，请重启应用程序。")
                else:
                    self.append_line("[更新内核] 未找到 webui 目录")
            except Exception as e:
                self.append_line(f"[更新内核] 执行 git 命令时出错：{str(e)}")

    def _small_btn_style(self):
        return f"""
            QPushButton {{
                background-color: {COLORS['bg_hover']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent']}; color: white; }}
        """
