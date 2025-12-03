"""
后台工作线程
负责异步执行Wiki爬取任务
"""
from PyQt5.QtCore import QThread, pyqtSignal
from feishu_api import FeishuAPI


class WikiWorkerThread(QThread):
    """Wiki爬取工作线程"""
    
    # 定义信号
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, app_id: str, app_secret: str, wiki_link: str, save_path: str, 
                 export_formats: list = None, use_parallel: bool = True, max_workers: int = 3,
                 turbo_mode: bool = False):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.wiki_link = wiki_link
        self.save_path = save_path
        self.export_formats = export_formats or ['md']
        self.use_parallel = use_parallel
        self.max_workers = max_workers
        self.turbo_mode = turbo_mode
    
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
            if self.turbo_mode:
                # 极速模式 - 使用异步爬取器
                from async_exporter import AsyncParallelWikiCrawler
                crawler = AsyncParallelWikiCrawler(api, self.export_formats, self.max_workers)
                self.log_signal.emit(f"🚀 极速模式 (并发数: {self.max_workers})")
            elif self.use_parallel:
                from parallel_crawler import ParallelWikiCrawler
                crawler = ParallelWikiCrawler(api, self.export_formats, self.max_workers)
                self.log_signal.emit(f"⚡ 并行模式 (并行数: {self.max_workers})")
            else:
                from wiki_crawler import WikiCrawler
                crawler = WikiCrawler(api, self.export_formats)
                self.log_signal.emit("📊 串行模式")
            
            self.progress_signal.emit(30)
            
            # 开始爬取
            count, error = crawler.crawl_wiki(
                self.wiki_link,
                self.save_path
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
