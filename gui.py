"""
GUI界面模块
使用PyQt5实现图形用户界面
"""
import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QGroupBox, QProgressBar, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

from feishu_api import FeishuAPI
from markdown_converter import MarkdownConverter


class WorkerThread(QThread):
    """后台工作线程，避免阻塞UI"""
    
    # 定义信号
    log_signal = pyqtSignal(str)  # 日志信号
    progress_signal = pyqtSignal(int)  # 进度信号
    finished_signal = pyqtSignal(bool, str)  # 完成信号（成功/失败，消息）
    
    def __init__(self, app_id: str, app_secret: str, share_link: str, save_path: str):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.share_link = share_link
        self.save_path = save_path
    
    def run(self):
        """执行爬取任务"""
        try:
            # 初始化API客户端
            self.log_signal.emit("🚀 初始化飞书API客户端...")
            api = FeishuAPI(self.app_id, self.app_secret)
            self.progress_signal.emit(10)
            
            # 获取access_token
            self.log_signal.emit("🔑 正在获取access_token...")
            token = api.get_tenant_access_token()
            if not token:
                self.finished_signal.emit(False, "获取access_token失败，请检查App ID和App Secret")
                return
            self.progress_signal.emit(30)
            
            # 提取文档ID
            self.log_signal.emit("📄 正在解析文档链接...")
            doc_id = api.extract_document_id(self.share_link)
            if not doc_id:
                self.finished_signal.emit(False, "无法从链接中提取文档ID，请检查链接格式")
                return
            self.log_signal.emit(f"✅ 文档ID: {doc_id}")
            self.progress_signal.emit(40)
            
            # 获取文档元数据
            self.log_signal.emit("📊 正在获取文档信息...")
            metadata = api.get_document_metadata(doc_id)
            doc_title = "未命名文档"
            if metadata:
                doc_title = metadata.get("title", "未命名文档")
                self.log_signal.emit(f"📌 文档标题: {doc_title}")
            self.progress_signal.emit(50)
            
            # 获取文档内容
            self.log_signal.emit("📥 正在下载文档内容...")
            content = api.get_document_content(doc_id)
            if not content:
                self.finished_signal.emit(False, "获取文档内容失败，请检查权限或文档ID")
                return
            self.progress_signal.emit(70)
            
            # 转换为Markdown
            self.log_signal.emit("🔄 正在转换为Markdown格式...")
            converter = MarkdownConverter()
            markdown_text = converter.convert(content, metadata)
            self.progress_signal.emit(85)
            
            # 保存文件
            self.log_signal.emit("💾 正在保存文件...")
            # 清理文件名中的非法字符
            safe_title = self._sanitize_filename(doc_title)
            filename = f"{safe_title}.md"
            filepath = os.path.join(self.save_path, filename)
            
            # 如果文件已存在，添加时间戳
            if os.path.exists(filepath):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{safe_title}_{timestamp}.md"
                filepath = os.path.join(self.save_path, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            
            self.progress_signal.emit(100)
            self.log_signal.emit(f"✅ 文件已保存至: {filepath}")
            self.finished_signal.emit(True, f"成功！文件已保存至:\n{filepath}")
            
        except Exception as e:
            self.log_signal.emit(f"❌ 错误: {str(e)}")
            self.finished_signal.emit(False, f"发生错误: {str(e)}")
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名中的非法字符"""
        # 移除或替换Windows文件名中的非法字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename.strip()


class BatchWorkerThread(QThread):
    """批量链接爬取工作线程"""
    
    # 定义信号
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, app_id: str, app_secret: str, links_text: str, save_path: str):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.links_text = links_text
        self.save_path = save_path
    
    def run(self):
        """执行批量爬取任务"""
        try:
            # 初始化API客户端
            self.log_signal.emit("🚀 初始化飞书API客户端...")
            api = FeishuAPI(self.app_id, self.app_secret)
            self.progress_signal.emit(10)
            
            # 获取access_token
            self.log_signal.emit("🔑 正在获取access_token...")
            token = api.get_tenant_access_token()
            if not token:
                self.finished_signal.emit(False, "获取access_token失败，请检查App ID和App Secret")
                return
            self.progress_signal.emit(20)
            
            # 初始化批量爬取器
            from batch_crawler import BatchCrawler
            crawler = BatchCrawler(api)
            
            # 定义进度回调
            def progress_callback(message):
                self.log_signal.emit(message)
            
            self.progress_signal.emit(30)
            
            # 开始批量爬取
            success, fail, error = crawler.crawl_batch(
                self.links_text,
                self.save_path,
                progress_callback
            )
            
            self.progress_signal.emit(100)
            
            if error:
                self.finished_signal.emit(False, f"爬取失败: {error}")
            elif success > 0:
                msg = f"🎉 批量爬取完成！\n✅ 成功: {success} 篇"
                if fail > 0:
                    msg += f"\n❌ 失败: {fail} 篇"
                self.finished_signal.emit(True, msg)
            else:
                self.finished_signal.emit(False, "所有文档都爬取失败")
                
        except Exception as e:
            self.log_signal.emit(f"❌ 错误: {str(e)}")
            self.finished_signal.emit(False, f"发生错误: {str(e)}")


class WikiWorkerThread(QThread):
    """Wiki自动爬取工作线程（实验性）"""
    
    # 定义信号
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, app_id: str, app_secret: str, wiki_link: str, save_path: str):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.wiki_link = wiki_link
        self.save_path = save_path
    
    def run(self):
        """执行Wiki批量爬取任务"""
        try:
            # 初始化API客户端
            self.log_signal.emit("🚀 初始化飞书API客户端...")
            api = FeishuAPI(self.app_id, self.app_secret)
            self.progress_signal.emit(10)
            
            # 获取access_token
            self.log_signal.emit("🔑 正在获取access_token...")
            token = api.get_tenant_access_token()
            if not token:
                self.finished_signal.emit(False, "获取access_token失败，请检查App ID和App Secret")
                return
            self.progress_signal.emit(20)
            
            # 初始化Wiki爬取器
            from wiki_crawler import WikiCrawler
            crawler = WikiCrawler(api)
            
            # 定义进度回调
            def progress_callback(message):
                self.log_signal.emit(message)
            
            self.progress_signal.emit(30)
            
            # 开始爬取
            count, error = crawler.crawl_wiki(
                self.wiki_link,
                self.save_path,
                progress_callback
            )
            
            self.progress_signal.emit(100)
            
            if error:
                self.finished_signal.emit(False, f"爬取失败: {error}")
            elif count > 0:
                self.finished_signal.emit(True, f"🎉 爬取完成！共导出 {count} 篇文档")
            else:
                self.finished_signal.emit(False, "未找到任何文档")
                
        except Exception as e:
            self.log_signal.emit(f"❌ 错误: {str(e)}")
            self.finished_signal.emit(False, f"发生错误: {str(e)}")


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.config = self._load_config()
        self.worker_thread = None
        self._init_logging()
        self._init_ui()
    
    def _init_logging(self):
        """初始化日志"""
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'feishu_crawler_{datetime.now().strftime("%Y%m%d")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        # 尝试加载本地配置
        local_config_path = os.path.join(os.path.dirname(__file__), 'config_local.json')
        if os.path.exists(local_config_path):
            config_path = local_config_path
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            return {
                "app_id": "",
                "app_secret": "",
                "default_save_path": str(Path.home() / "Desktop")
            }
    
    def _save_config(self):
        """保存配置到本地配置文件"""
        local_config_path = os.path.join(os.path.dirname(__file__), 'config_local.json')
        
        config = {
            "app_id": self.app_id_input.text().strip(),
            "app_secret": self.app_secret_input.text().strip(),
            "default_save_path": self.save_path_input.text().strip()
        }
        
        try:
            with open(local_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"保存配置文件失败: {e}")
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("DocHarvest v1.0")
        self.setGeometry(100, 100, 800, 700)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 标题
        title_label = QLabel("📄 飞书文档爬取工具")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 配置区域
        config_group = QGroupBox("⚙️ 配置信息")
        config_layout = QVBoxLayout()
        
        # App ID
        app_id_layout = QHBoxLayout()
        app_id_layout.addWidget(QLabel("App ID:"))
        self.app_id_input = QLineEdit()
        self.app_id_input.setText(self.config.get("app_id", ""))
        self.app_id_input.setPlaceholderText("请输入飞书应用的App ID")
        app_id_layout.addWidget(self.app_id_input)
        config_layout.addLayout(app_id_layout)
        
        # App Secret
        app_secret_layout = QHBoxLayout()
        app_secret_layout.addWidget(QLabel("App Secret:"))
        self.app_secret_input = QLineEdit()
        self.app_secret_input.setText(self.config.get("app_secret", ""))
        self.app_secret_input.setPlaceholderText("请输入飞书应用的App Secret")
        self.app_secret_input.setEchoMode(QLineEdit.Password)
        app_secret_layout.addWidget(self.app_secret_input)
        config_layout.addLayout(app_secret_layout)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # 爬取模式选择
        mode_group = QGroupBox("📑 爬取模式")
        mode_layout = QVBoxLayout()
        
        # 创建单选按钮组
        self.mode_button_group = QButtonGroup()
        
        self.single_mode_radio = QRadioButton("单文档爬取")
        self.single_mode_radio.setChecked(True)
        self.single_mode_radio.setToolTip("爬取单个飞书文档")
        self.mode_button_group.addButton(self.single_mode_radio, 1)
        
        self.batch_mode_radio = QRadioButton("批量链接爬取（推荐）")
        self.batch_mode_radio.setToolTip("一次性输入多个文档链接，批量爬取")
        self.mode_button_group.addButton(self.batch_mode_radio, 2)
        
        self.wiki_mode_radio = QRadioButton("Wiki自动爬取（实验性）")
        self.wiki_mode_radio.setToolTip("输入Wiki链接，自动爬取（需要特殊权限）")
        self.mode_button_group.addButton(self.wiki_mode_radio, 3)
        
        mode_layout.addWidget(self.single_mode_radio)
        mode_layout.addWidget(self.batch_mode_radio)
        mode_layout.addWidget(self.wiki_mode_radio)
        
        # 添加模式切换提示
        mode_hint = QLabel("💡 推荐使用「批量链接爬取」：复制所有文档链接，一次性粘贴即可")
        mode_hint.setStyleSheet("color: #666; font-size: 11px;")
        mode_hint.setWordWrap(True)
        mode_layout.addWidget(mode_hint)
        
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)
        
        # 文档链接输入
        link_group = QGroupBox("🔗 文档/Wiki链接")
        link_layout = QVBoxLayout()
        
        # 使用QTextEdit支持多行输入
        self.link_input = QTextEdit()
        self.link_input.setPlaceholderText(
            "请粘贴飞书文档链接：\n"
            "• 单文档模式：输入一个链接\n"
            "• 批量模式：每行一个链接（推荐）\n"
            "• Wiki模式：输入Wiki链接"
        )
        self.link_input.setMaximumHeight(120)
        link_layout.addWidget(self.link_input)
        
        # 添加示例提示
        example_label = QLabel(
            "示例:\n"
            "• 单文档: https://xxx.feishu.cn/docx/xxxxx\n"
            "• 批量链接: 一行一个链接，可粘贴多个\n"
            "• Wiki: https://xxx.feishu.cn/wiki/xxxxx"
        )
        example_label.setStyleSheet("color: #888; font-size: 10px;")
        link_layout.addWidget(example_label)
        
        link_group.setLayout(link_layout)
        main_layout.addWidget(link_group)
        
        # 保存路径
        path_group = QGroupBox("💾 保存路径")
        path_layout = QHBoxLayout()
        
        self.save_path_input = QLineEdit()
        default_path = self.config.get("default_save_path", "")
        if not default_path:
            default_path = str(Path.home() / "Desktop")
        self.save_path_input.setText(default_path)
        path_layout.addWidget(self.save_path_input)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self._browse_folder)
        path_layout.addWidget(browse_btn)
        
        path_group.setLayout(path_layout)
        main_layout.addWidget(path_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # 开始按钮
        self.start_btn = QPushButton("🚀 开始爬取")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_btn.clicked.connect(self._start_crawl)
        main_layout.addWidget(self.start_btn)
        
        # 日志区域
        log_group = QGroupBox("📋 运行日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #f5f5f5;")
        log_layout.addWidget(self.log_text)
        
        # 清除日志按钮
        clear_log_btn = QPushButton("清除日志")
        clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        log_layout.addWidget(clear_log_btn)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
    
    def _browse_folder(self):
        """浏览选择保存文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择保存目录",
            self.save_path_input.text()
        )
        if folder:
            self.save_path_input.setText(folder)
    
    def _append_log(self, message: str):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        # 自动滚动到底部
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def _start_crawl(self):
        """开始爬取"""
        # 验证输入
        app_id = self.app_id_input.text().strip()
        app_secret = self.app_secret_input.text().strip()
        share_link = self.link_input.toPlainText().strip()  # QTextEdit使用toPlainText()
        save_path = self.save_path_input.text().strip()
        
        if not app_id or not app_secret:
            QMessageBox.warning(self, "警告", "请先填写App ID和App Secret")
            return
        
        if not share_link:
            QMessageBox.warning(self, "警告", "请输入飞书文档/Wiki链接")
            return
        
        if not save_path or not os.path.exists(save_path):
            QMessageBox.warning(self, "警告", "请选择有效的保存路径")
            return
        
        # 获取选择的模式
        is_batch_mode = self.batch_mode_radio.isChecked()
        is_wiki_mode = self.wiki_mode_radio.isChecked()
        
        # 批量模式检查链接数量
        if is_batch_mode:
            lines = [l.strip() for l in share_link.split('\n') if l.strip()]
            if len(lines) < 2:
                reply = QMessageBox.question(
                    self,
                    "确认模式",
                    "批量链接爬取模式需要输入多个链接（每行一个）。\n"
                    "只有一个链接时建议使用「单文档爬取」模式。\n\n"
                    "是否继续使用批量模式？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
        
        # Wiki模式提示
        if is_wiki_mode:
            reply = QMessageBox.question(
                self, 
                "确认Wiki爬取", 
                "⚠️ Wiki自动爬取功能为实验性功能，可能需要特殊权限。\n\n"
                "如果爬取失败，建议使用「批量链接爬取」模式。\n\n"
                "确定要继续吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.No:
                return
        
        # 保存配置
        self._save_config()
        
        # 禁用按钮
        self.start_btn.setEnabled(False)
        if is_batch_mode:
            self.start_btn.setText("⏳ 批量爬取中...")
        elif is_wiki_mode:
            self.start_btn.setText("⏳ Wiki爬取中...")
        else:
            self.start_btn.setText("⏳ 爬取中...")
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        # 根据模式创建不同的工作线程
        if is_batch_mode:
            # 批量链接爬取
            self.worker_thread = BatchWorkerThread(app_id, app_secret, share_link, save_path)
        elif is_wiki_mode:
            # Wiki自动爬取
            self.worker_thread = WikiWorkerThread(app_id, app_secret, share_link, save_path)
        else:
            # 单文档爬取
            self.worker_thread = WorkerThread(app_id, app_secret, share_link, save_path)
        
        # 连接信号
        self.worker_thread.log_signal.connect(self._append_log)
        self.worker_thread.progress_signal.connect(self.progress_bar.setValue)
        self.worker_thread.finished_signal.connect(self._on_finished)
        self.worker_thread.start()
    
    def _on_finished(self, success: bool, message: str):
        """爬取完成回调"""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🚀 开始爬取")
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.statusBar().showMessage("爬取完成")
        else:
            QMessageBox.critical(self, "失败", message)
            self.statusBar().showMessage("爬取失败")


def run_app():
    """运行应用"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion样式，更现代
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()

