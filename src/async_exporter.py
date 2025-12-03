"""
异步飞书导出器 - 极速版本
使用aiohttp实现异步并发,大幅提升速度
目标: 100-200篇文档在60秒内完成
"""
import os
import time
import logging
import asyncio
import aiohttp
from typing import Optional, Dict, Any, Tuple, List


class AsyncFeishuExporter:
    """异步飞书导出器 - 使用aiohttp实现高并发"""
    
    def __init__(self, api):
        """
        初始化异步导出器
        
        Args:
            api: FeishuAPI实例
        """
        self.api = api
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://open.feishu.cn/open-apis"
        
        # 配置连接池
        self.connector = None
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器 - 进入"""
        # 创建连接池 - 允许更多并发连接
        self.connector = aiohttp.TCPConnector(
            limit=50,  # 最大连接数
            limit_per_host=20,  # 每个主机最大连接数
            ttl_dns_cache=300,  # DNS缓存时间
            force_close=False,  # 保持连接
            enable_cleanup_closed=True
        )
        
        # 创建会话 - 配置超时
        timeout = aiohttp.ClientTimeout(
            total=120,  # 总超时
            connect=10,  # 连接超时
            sock_read=30  # 读取超时
        )
        
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {self.api.access_token}",
                "Content-Type": "application/json; charset=utf-8"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器 - 退出"""
        if self.session:
            await self.session.close()
        if self.connector:
            await self.connector.close()
    
    async def export_document_batch(
        self, 
        doc_token: str, 
        doc_type: str, 
        export_formats: List[str], 
        base_path: str, 
        filename: str
    ) -> Dict[str, Tuple[bool, str]]:
        """
        异步批量导出文档（真正并发）
        
        Args:
            doc_token: 文档token
            doc_type: 文档类型
            export_formats: 导出格式列表
            base_path: 保存目录
            filename: 文件名
            
        Returns:
            {格式: (成功, 错误信息)}
        """
        if not self.session:
            return {fmt: (False, "会话未初始化") for fmt in export_formats}
        
        # 并发创建所有导出任务
        tasks = [
            self._export_single_format(doc_token, doc_type, fmt, base_path, filename)
            for fmt in export_formats
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 组装结果
        output = {}
        for fmt, result in zip(export_formats, results):
            if isinstance(result, Exception):
                output[fmt] = (False, str(result))
            else:
                output[fmt] = result
        
        return output
    
    async def _export_single_format(
        self,
        doc_token: str,
        doc_type: str,
        export_format: str,
        base_path: str,
        filename: str
    ) -> Tuple[bool, str]:
        """
        异步导出单个格式
        
        Returns:
            (成功, 错误信息)
        """
        try:
            # 步骤1: 创建导出任务
            ticket = await self._create_export_task(doc_token, doc_type, export_format)
            if not ticket:
                return (False, "创建任务失败")
            
            # 步骤2: 轮询任务结果（优化轮询间隔）
            file_token = await self._query_export_result(ticket, doc_token)
            if not file_token:
                return (False, "查询任务失败或超时")
            
            # 步骤3: 下载文件
            save_path = os.path.join(base_path, f"{filename}.{export_format}")
            success = await self._download_exported_file(file_token, save_path)
            
            if success:
                return (True, "")
            else:
                return (False, "下载失败")
        
        except Exception as e:
            return (False, str(e))
    
    async def _create_export_task(
        self, 
        doc_token: str, 
        doc_type: str, 
        export_format: str
    ) -> Optional[str]:
        """
        异步创建导出任务
        
        Returns:
            任务ticket或None
        """
        url = f"{self.base_url}/drive/v1/export_tasks"
        
        type_mapping = {
            "doc": "doc",
            "docx": "docx",
            "sheet": "sheet",
            "bitable": "bitable"
        }
        
        payload = {
            "file_extension": export_format,
            "token": doc_token,
            "type": type_mapping.get(doc_type, "docx")
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                result = await response.json()
                
                if result.get("code") == 0:
                    ticket = result.get("data", {}).get("ticket")
                    self.logger.info(f"✓ 创建{export_format.upper()}任务: {ticket}")
                    return ticket
                else:
                    error_msg = result.get('msg', 'Unknown error')
                    self.logger.error(f"创建任务失败: {error_msg}")
                    return None
        
        except Exception as e:
            self.logger.error(f"创建任务异常: {str(e)}")
            return None
    
    async def _query_export_result(
        self, 
        ticket: str, 
        doc_token: str, 
        max_wait: int = 60
    ) -> Optional[str]:
        """
        异步查询导出结果（优化轮询策略）
        
        Returns:
            file_token或None
        """
        url = f"{self.base_url}/drive/v1/export_tasks/{ticket}"
        params = {"token": doc_token}
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < max_wait:
            try:
                async with self.session.get(url, params=params) as response:
                    result = await response.json()
                    
                    if result.get("code") == 0:
                        data = result.get("data", {})
                        result_data = data.get("result", data)
                        
                        job_status = result_data.get("job_status")
                        
                        # 成功
                        if job_status in [0, "success"]:
                            file_token = (
                                result_data.get("file_token") or 
                                result_data.get("token") or
                                result_data.get("ticket")
                            )
                            
                            if file_token and file_token.strip():
                                return file_token.strip()
                            
                            # 任务成功但token为空,继续等待
                            await asyncio.sleep(0.3)
                        
                        # 失败
                        elif job_status in [3, "failed"]:
                            error_msg = data.get("job_error_msg", "Unknown error")
                            self.logger.error(f"导出失败: {error_msg}")
                            return None
                        
                        # 进行中 - 激进轮询策略
                        else:
                            check_count += 1
                            if check_count <= 5:
                                await asyncio.sleep(0.2)  # 前5次快速检查
                            elif check_count <= 10:
                                await asyncio.sleep(0.5)  # 6-10次中速
                            else:
                                await asyncio.sleep(1)    # 之后正常间隔
                    else:
                        self.logger.error(f"查询失败: {result.get('msg')}")
                        return None
            
            except asyncio.TimeoutError:
                self.logger.warning("查询超时,重试...")
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.warning(f"查询异常,重试: {str(e)}")
                await asyncio.sleep(1)
        
        self.logger.error("导出超时")
        return None
    
    async def _download_exported_file(
        self, 
        file_token: str, 
        save_path: str
    ) -> bool:
        """
        异步下载文件
        
        Returns:
            是否成功
        """
        url = f"{self.base_url}/drive/v1/export_tasks/file/{file_token}/download"
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.logger.error(f"下载失败: HTTP {response.status}")
                    return False
                
                # 确保目录存在
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # 异步写入文件
                with open(save_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                
                self.logger.info(f"✓ 已下载: {os.path.basename(save_path)}")
                return True
        
        except Exception as e:
            self.logger.error(f"下载异常: {str(e)}")
            return False


class AsyncParallelWikiCrawler:
    """
    异步并行Wiki爬取器 - 极速版本
    使用异步I/O + 高并发实现极致性能
    """
    
    def __init__(self, api, export_formats: List[str] = None, max_workers: int = 10):
        """
        Args:
            api: FeishuAPI实例
            export_formats: 导出格式列表
            max_workers: 最大并发数（建议10-20）
        """
        self.api = api
        self.export_formats = export_formats or ['pdf']
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
        self.crawled_nodes = set()
        self.semaphore = None  # 并发控制信号量
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        filename = filename.strip()
        if len(filename) > 100:
            filename = filename[:100]
        return filename or "未命名"
    
    async def _process_document_node(
        self, 
        node: Dict[str, Any], 
        base_path: str,
        exporter: AsyncFeishuExporter,
        level: int = 0
    ) -> int:
        """
        异步处理单个文档节点
        
        Returns:
            成功数量（0或1）
        """
        title = node.get("title", "未命名")
        node_token = node.get("node_token")
        obj_token = node.get("obj_token", "")
        obj_type = node.get("obj_type", "")
        node_type = node.get("node_type")
        
        safe_title = self._sanitize_filename(title)
        exported_any = False
        
        # 处理Markdown格式（同步获取内容）
        if 'md' in self.export_formats:
            try:
                content = self.api.get_document_content(node_token)
                if content:
                    from document_converter import DocumentConverter
                    converter = DocumentConverter()
                    metadata = {"title": title}
                    markdown_text = converter.to_markdown(content, metadata)
                    file_path = os.path.join(base_path, f"{safe_title}.md")
                    
                    # 确保目录存在
                    os.makedirs(base_path, exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_text)
                    
                    self.logger.info(f"{'  ' * level}✅ MD: {safe_title}.md")
                    exported_any = True
                else:
                    self.logger.warning(f"{'  ' * level}⚠️ MD获取内容失败: {title}")
            except Exception as e:
                self.logger.error(f"{'  ' * level}❌ MD导出失败: {title} - {str(e)}")
        
        # 处理PDF和Word（使用异步导出器）
        native_formats = [fmt for fmt in self.export_formats if fmt in ['docx', 'pdf']]
        
        if native_formats:
            export_token = obj_token if obj_token else node_token
            export_type = obj_type if obj_type else (node_type or "docx")
            
            # 使用异步导出器
            os.makedirs(base_path, exist_ok=True)
            results = await exporter.export_document_batch(
                export_token,
                export_type,
                native_formats,
                base_path,
                safe_title
            )
            
            # 检查结果
            for fmt, (success, error) in results.items():
                if success:
                    self.logger.info(f"{'  ' * level}✅ {fmt.upper()}: {safe_title}.{fmt}")
                    exported_any = True
                else:
                    self.logger.warning(f"{'  ' * level}❌ {fmt.upper()}失败: {error}")
        
        if exported_any:
            return 1
        else:
            self.logger.warning(f"{'  ' * level}❌ 所有格式导出失败: {title}")
            return 0
    
    async def _crawl_node_async(
        self,
        node: Dict[str, Any],
        base_path: str,
        space_id: str,
        exporter: AsyncFeishuExporter,
        level: int = 0
    ) -> int:
        """
        异步递归爬取节点
        
        Returns:
            成功文档数
        """
        node_token = node.get("node_token")
        title = node.get("title", "未命名")
        has_child = node.get("has_child", False)
        
        # 避免重复
        if node_token in self.crawled_nodes:
            return 0
        self.crawled_nodes.add(node_token)
        
        count = 0
        
        # 处理当前文档
        node_type = node.get("node_type")
        obj_type = node.get("obj_type", "")
        
        if node_type in ["doc", "docx"] or obj_type in ["doc", "docx"]:
            # 使用信号量控制并发
            async with self.semaphore:
                count += await self._process_document_node(node, base_path, exporter, level)
        
        # 处理子节点
        if has_child:
            safe_title = self._sanitize_filename(title)
            sub_dir = os.path.join(base_path, safe_title)
            os.makedirs(sub_dir, exist_ok=True)
            
            # 同步获取子节点（这部分API不支持异步）
            from wiki_crawler import WikiCrawler
            temp_crawler = WikiCrawler(self.api, self.export_formats)
            child_nodes = temp_crawler.get_child_nodes(space_id, node_token)
            
            if child_nodes:
                # 异步并发处理所有子节点
                tasks = [
                    self._crawl_node_async(child, sub_dir, space_id, exporter, level + 1)
                    for child in child_nodes
                ]
                child_counts = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in child_counts:
                    if isinstance(result, int):
                        count += result
                    else:
                        self.logger.error(f"子节点处理失败: {result}")
        
        return count
    
    async def crawl_wiki_async(self, wiki_link: str, save_path: str) -> Tuple[int, str]:
        """
        异步爬取Wiki
        
        Returns:
            (成功数量, 错误信息)
        """
        try:
            # 提取space_id
            from wiki_crawler import WikiCrawler
            temp_crawler = WikiCrawler(self.api, self.export_formats)
            space_id = temp_crawler.extract_space_id_from_link(wiki_link)
            
            if not space_id:
                return (0, "无法提取space_id")
            
            self.logger.info(f"🚀 开始极速爬取: {space_id}")
            self.logger.info(f"⚡ 并发数: {self.max_workers}")
            self.logger.info(f"📤 格式: {', '.join(self.export_formats)}")
            
            # 获取根节点
            root_nodes = temp_crawler.get_child_nodes(space_id, None)
            if not root_nodes:
                return (0, "无法获取根节点")
            
            # 创建输出目录
            output_dir = os.path.join(save_path, f"Wiki导出_{int(time.time())}")
            os.makedirs(output_dir, exist_ok=True)
            
            # 创建信号量控制并发
            self.semaphore = asyncio.Semaphore(self.max_workers)
            
            # 使用异步导出器
            async with AsyncFeishuExporter(self.api) as exporter:
                # 并发处理所有根节点
                tasks = [
                    self._crawl_node_async(node, output_dir, space_id, exporter, 0)
                    for node in root_nodes
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                total_count = 0
                for result in results:
                    if isinstance(result, int):
                        total_count += result
                    else:
                        self.logger.error(f"根节点处理失败: {result}")
            
            self.logger.info(f"🎉 完成! 共 {total_count} 篇文档")
            self.logger.info(f"📂 位置: {output_dir}")
            
            return (total_count, "")
        
        except Exception as e:
            error_msg = f"爬取失败: {str(e)}"
            self.logger.error(error_msg)
            import traceback
            traceback.print_exc()
            return (0, error_msg)
    
    def crawl_wiki(self, wiki_link: str, save_path: str) -> Tuple[int, str]:
        """
        同步包装器 - 运行异步爬取
        
        Returns:
            (成功数量, 错误信息)
        """
        # 创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(
                self.crawl_wiki_async(wiki_link, save_path)
            )
        finally:
            loop.close()
