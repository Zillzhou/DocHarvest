
import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from feishu_api import FeishuAPI
from workers import WikiWorkerThread



class AppleColors:

    # System colors
    SYSTEM_BLUE = QColor(0, 122, 255)
    SYSTEM_GREEN = QColor(52, 199, 89)
    SYSTEM_RED = QColor(255, 59, 48)
    SYSTEM_ORANGE = QColor(255, 149, 0)
    SYSTEM_GRAY = QColor(142, 142, 147)
    
    # Background colors
    BG_PRIMARY = QColor(255, 255, 255)
    BG_SECONDARY = QColor(248, 248, 248)
    BG_TERTIARY = QColor(242, 242, 247)
    
    # Label colors
    LABEL_PRIMARY = QColor(0, 0, 0)
    LABEL_SECONDARY = QColor(60, 60, 67, 153)  # 60% opacity
    LABEL_TERTIARY = QColor(60, 60, 67, 76)   # 30% opacity
    
    # Separator
    SEPARATOR = QColor(0, 0, 0, 13)  # 5% opacity
    
    # Vibrancy
    VIBRANCY_LIGHT = QColor(255, 255, 255, 230)


class AppleCard(QWidget):

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # 设置背景
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, AppleColors.BG_PRIMARY)
        self.setPalette(palette)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 10))
        self.setGraphicsEffect(shadow)


class AppleButton(QPushButton):

    
    def __init__(self, text, button_type='primary', parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setup_style()
        self.setCursor(Qt.PointingHandCursor)
    
    def setup_style(self):
        if self.button_type == 'primary':
            bg_color = AppleColors.SYSTEM_BLUE
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb({bg_color.red()}, {bg_color.green()}, {bg_color.blue()});
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 11px 20px;
                    font-size: 15px;
                    font-weight: 500;
                    font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                }}
                QPushButton:hover {{
                    background-color: rgb(0, 112, 245);
                }}
                QPushButton:pressed {{
                    background-color: rgb(0, 102, 235);
                }}
                QPushButton:disabled {{
                    background-color: rgb(142, 142, 147, 80);
                    color: rgba(255, 255, 255, 0.5);
                }}
            """)
        elif self.button_type == 'secondary':
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgb(242, 242, 247);
                    color: rgb(0, 122, 255);
                    border: none;
                    border-radius: 10px;
                    padding: 11px 20px;
                    font-size: 15px;
                    font-weight: 500;
                    font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                }
                QPushButton:hover {
                    background-color: rgb(235, 235, 240);
                }
                QPushButton:pressed {
                    background-color: rgb(225, 225, 230);
                }
            """)


class AppleLineEdit(QLineEdit):

    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setup_style()
    
    def setup_style(self):
        self.setStyleSheet("""
            QLineEdit {
                background-color: rgb(248, 248, 248);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 15px;
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                color: rgb(0, 0, 0);
                selection-background-color: rgb(0, 122, 255);
            }
            QLineEdit:focus {
                background-color: white;
                border: 2px solid rgb(0, 122, 255);
                padding: 9px 13px;
            }
            QLineEdit:hover {
                background-color: rgb(245, 245, 245);
            }
        """)


class AppleTextEdit(QTextEdit):

    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setup_style()
    
    def setup_style(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: rgb(248, 248, 248);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 15px;
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                color: rgb(0, 0, 0);
                selection-background-color: rgb(0, 122, 255);
            }
            QTextEdit:focus {
                background-color: white;
                border: 2px solid rgb(0, 122, 255);
                padding: 9px 13px;
            }
        """)


class AppleCheckBox(QCheckBox):

    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setup_style()
        self.setCursor(Qt.PointingHandCursor)
    
    def setup_style(self):
        self.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
                font-size: 15px;
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                color: rgb(0, 0, 0);
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 1.5px solid rgba(0, 0, 0, 0.2);
                background-color: white;
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid rgb(0, 122, 255);
                background-color: rgb(248, 248, 248);
            }
            QCheckBox::indicator:checked {
                background-color: rgb(0, 122, 255);
                border: 1.5px solid rgb(0, 122, 255);
                image: url(none);
            }
            QCheckBox::indicator:checked:hover {
                background-color: rgb(0, 112, 245);
            }
        """)


class AppleMainWindow(QMainWindow):

    
    def __init__(self):
        super().__init__()
        self.config = self._load_config()
        self.worker_thread = None
        self._init_logging()
        self._init_ui()
        self._fade_in()
    
    def _init_logging(self):
        root_dir = os.path.dirname(os.path.dirname(__file__))
        log_dir = os.path.join(root_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'harvest_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def _load_config(self):
        root_dir = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(root_dir, 'config_local.json')
        if not os.path.exists(config_path):
            config_path = os.path.join(root_dir, 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "app_id": "",
                "app_secret": "",
                "default_save_path": str(Path.home() / "Desktop")
            }
    
    def _save_config(self):
        root_dir = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(root_dir, 'config_local.json')
        config = {
            "app_id": self.app_id_input.text().strip(),
            "app_secret": self.app_secret_input.text().strip(),
            "default_save_path": self.save_path_input.text().strip()
        }
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"保存配置失败: {e}")
    
    def _init_ui(self):
        self.setWindowTitle("DocHarvest")
        self.setGeometry(100, 100, 760, 840)
        
        # 设置窗口背景色
        palette = self.palette()
        palette.setColor(QPalette.Window, AppleColors.BG_SECONDARY)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # 中央容器
        central = QWidget()
        self.setCentralWidget(central)
        
        # 主布局 - 使用网格对齐
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)
        
        # 标题区域
        self._create_header(main_layout)
        
        # 认证卡片
        self._create_auth_section(main_layout)
        
        # 导出配置卡片
        self._create_export_section(main_layout)
        
        # 导出按钮
        self._create_export_button(main_layout)
        
        # 日志区域
        self._create_console_section(main_layout)
        
        main_layout.addStretch()
    
    def _create_header(self, parent_layout):
        """创建标题区域"""
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        
        # App 图标 + 标题
        title_row = QHBoxLayout()
        
        # 图标
        icon_label = QLabel("📄")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 42px;
                padding: 0px;
            }
        """)
        title_row.addWidget(icon_label)
        
        title_row.addSpacing(12)
        
        # 标题
        title = QLabel("DocHarvest")
        title.setStyleSheet("""
            QLabel {
                font-size: 34px;
                font-weight: 600;
                color: rgb(0, 0, 0);
                font-family: -apple-system, 'SF Pro Display', 'Segoe UI', system-ui;
            }
        """)
        title_row.addWidget(title)
        title_row.addStretch()
        
        header_layout.addLayout(title_row)
        
        # 副标题
        subtitle = QLabel("飞书文档批量导出")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 17px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        header_layout.addWidget(subtitle)
        
        parent_layout.addWidget(header)
    
    def _create_auth_section(self, parent_layout):
        """创建认证区域"""
        card = AppleCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(16)
        
        # 标题
        section_title = QLabel("飞书应用凭证")
        section_title.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: 600;
                color: rgb(0, 0, 0);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        card_layout.addWidget(section_title)
        
        # App ID
        id_label = QLabel("App ID")
        id_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        card_layout.addWidget(id_label)
        
        self.app_id_input = AppleLineEdit("cli_xxxxxxxxxxxxxxxx")
        self.app_id_input.setText(self.config.get("app_id", ""))
        card_layout.addWidget(self.app_id_input)
        
        # App Secret
        secret_label = QLabel("App Secret")
        secret_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                margin-top: 8px;
            }
        """)
        card_layout.addWidget(secret_label)
        
        self.app_secret_input = AppleLineEdit("请输入应用密钥")
        self.app_secret_input.setText(self.config.get("app_secret", ""))
        self.app_secret_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.app_secret_input)
        
        parent_layout.addWidget(card)
    
    def _create_export_section(self, parent_layout):
        """创建导出配置区域"""
        card = AppleCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(16)
        
        # 标题
        section_title = QLabel("导出配置")
        section_title.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: 600;
                color: rgb(0, 0, 0);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        card_layout.addWidget(section_title)
        
        # Wiki 链接
        link_label = QLabel("Wiki 分享链接")
        link_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        card_layout.addWidget(link_label)
        
        self.link_input = AppleTextEdit()
        self.link_input.setPlaceholderText("https://xxx.feishu.cn/wiki/xxxxx")
        self.link_input.setMaximumHeight(80)
        card_layout.addWidget(self.link_input)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(0, 0, 0, 0.05); max-height: 1px;")
        card_layout.addWidget(separator)
        
        # 导出格式
        format_label = QLabel("导出格式")
        format_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        card_layout.addWidget(format_label)
        
        format_layout = QHBoxLayout()
        format_layout.setSpacing(20)
        
        self.format_buttons = {}
        for fmt, label in [('pdf', 'PDF'), ('docx', 'Word'), ('md', 'Markdown')]:
            cb = AppleCheckBox(label)
            if fmt == 'pdf':
                cb.setChecked(True)
            format_layout.addWidget(cb)
            self.format_buttons[fmt] = cb
        
        format_layout.addStretch()
        card_layout.addLayout(format_layout)
        
        # 分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet("background-color: rgba(0, 0, 0, 0.05); max-height: 1px;")
        card_layout.addWidget(separator2)
        
        # 保存路径和并行数
        row = QHBoxLayout()
        row.setSpacing(16)
        
        # 左侧：保存路径
        left = QVBoxLayout()
        left.setSpacing(8)
        
        path_label = QLabel("保存位置")
        path_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        left.addWidget(path_label)
        
        path_row = QHBoxLayout()
        path_row.setSpacing(10)
        
        default_path = self.config.get("default_save_path", "") or str(Path.home() / "Desktop")
        self.save_path_input = AppleLineEdit()
        self.save_path_input.setText(default_path)
        path_row.addWidget(self.save_path_input)
        
        browse_btn = AppleButton("浏览", 'secondary')
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self._browse_folder)
        path_row.addWidget(browse_btn)
        
        left.addLayout(path_row)
        row.addLayout(left, 3)
        
        # 右侧：并行数
        right = QVBoxLayout()
        right.setSpacing(8)
        
        parallel_label = QLabel("并行数")
        parallel_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(60, 60, 67, 0.6);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        right.addWidget(parallel_label)
        
        self.workers_spinbox = QSpinBox()
        self.workers_spinbox.setMinimum(1)
        self.workers_spinbox.setMaximum(20)
        self.workers_spinbox.setValue(15)
        self.workers_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: rgb(248, 248, 248);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 15px;
                font-weight: 600;
                color: rgb(0, 122, 255);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                min-width: 80px;
            }
            QSpinBox:focus {
                background-color: white;
                border: 2px solid rgb(0, 122, 255);
                padding: 9px 13px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
            }
        """)
        right.addWidget(self.workers_spinbox)
        
        row.addLayout(right, 1)
        card_layout.addLayout(row)
        
        parent_layout.addWidget(card)
    
    def _create_export_button(self, parent_layout):
        """创建导出按钮"""
        self.export_btn = AppleButton("开始导出", 'primary')
        self.export_btn.setFixedHeight(50)
        self.export_btn.clicked.connect(self._start_export)
        parent_layout.addWidget(self.export_btn)
    
    def _create_console_section(self, parent_layout):
        """创建控制台日志区域"""
        card = AppleCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(12)
        
        # 标题栏
        header = QHBoxLayout()
        
        console_title = QLabel("控制台")
        console_title.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: 600;
                color: rgb(0, 0, 0);
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
            }
        """)
        header.addWidget(console_title)
        header.addStretch()
        
        clear_btn = QPushButton("清除")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgb(0, 122, 255);
                border: none;
                font-size: 15px;
                font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui;
                padding: 4px 8px;
            }
            QPushButton:hover {
                color: rgb(0, 112, 245);
            }
        """)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(lambda: self.log_text.clear())
        header.addWidget(clear_btn)
        
        card_layout.addLayout(header)
        
        # 日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: rgb(28, 28, 30);
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
                font-size: 13px;
                color: rgb(235, 235, 245);
                line-height: 1.5;
            }
        """)
        self.log_text.setMaximumHeight(160)
        card_layout.addWidget(self.log_text)
        
        parent_layout.addWidget(card)
    
    def _fade_in(self):
        """淡入动画"""
        self.setWindowOpacity(0)
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self.anim = anim
    
    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择保存目录", self.save_path_input.text())
        if folder:
            self.save_path_input.setText(folder)
    
    def _append_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        

        if "✅" in message or "成功" in message:
            color = "rgb(52, 199, 89)"
        elif "❌" in message or "失败" in message:
            color = "rgb(255, 59, 48)"
        elif "⚠️" in message or "警告" in message:
            color = "rgb(255, 149, 0)"
        elif "🚀" in message or "⚡" in message:
            color = "rgb(0, 122, 255)"
        else:
            color = "rgb(142, 142, 147)"
        
        html = f'<span style="color: rgb(142, 142, 147)">[{timestamp}]</span> <span style="color: {color}">{message}</span>'
        self.log_text.append(html)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
    
    def _start_export(self):
        app_id = self.app_id_input.text().strip()
        app_secret = self.app_secret_input.text().strip()
        wiki_link = self.link_input.toPlainText().strip()
        save_path = self.save_path_input.text().strip()
        
        if not app_id or not app_secret:
            QMessageBox.warning(self, "提示", "请填写应用凭证")
            return
        
        if not wiki_link:
            QMessageBox.warning(self, "提示", "请输入 Wiki 链接")
            return
        
        if not save_path or not os.path.exists(save_path):
            QMessageBox.warning(self, "提示", "请选择有效的保存路径")
            return
        
        export_formats = [fmt for fmt, cb in self.format_buttons.items() if cb.isChecked()]
        if not export_formats:
            QMessageBox.warning(self, "提示", "请至少选择一种导出格式")
            return
        
        self._save_config()
        
        self.export_btn.setEnabled(False)
        self.export_btn.setText("导出中...")
        self.log_text.clear()
        
        max_workers = self.workers_spinbox.value()
        
        self.worker_thread = WikiWorkerThread(
            app_id, app_secret, wiki_link, save_path,
            export_formats, True, max_workers, True
        )
        
        self.worker_thread.log_signal.connect(self._append_log)
        self.worker_thread.finished_signal.connect(self._on_finished)
        self.worker_thread.start()
    
    def _on_finished(self, success, message):
        self.export_btn.setEnabled(True)
        self.export_btn.setText("开始导出")
        
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.critical(self, "错误", message)


def run_apple_app():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 设置全局字体
    font = QFont("-apple-system")
    font.setFamily("SF Pro Text, Segoe UI, system-ui, sans-serif")
    app.setFont(font)
    
    window = AppleMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_apple_app()
