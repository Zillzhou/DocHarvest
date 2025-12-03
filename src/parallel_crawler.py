"""
并行Wiki爬取器 - 显著提升批量导出速度
使用多线程并行处理多个文档
"""
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from wiki_crawler import WikiCrawler


class ParallelWikiCrawler(WikiCrawler):
    """并行Wiki爬取器 - 多文档同时处理"""
    
    def __init__(self, api, export_formats: List[str] = None, max_workers: int = 3):
        """
        初始化并行爬取器
        
        Args:
            api: FeishuAPI实例
            export_formats: 导出格式列表
            max_workers: 最大并行数（建议2-5，太多可能被限流）
        """
        super().__init__(api, export_formats)
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
    
    def _process_single_node(self, node: Dict[str, Any], base_path: str, level: int = 0) -> int:
        """
        处理单个文档节点（不处理子节点）
        
        Args:
            node: 节点信息
            base_path: 保存路径
            level: 层级
            
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
        
        # 获取文档内容（仅用于Markdown导出）
        content = None
        if 'md' in self.export_formats:
            content = self.api.get_document_content(node_token)
        
        # Markdown导出
        if 'md' in self.export_formats:
            if content:
                from document_converter import DocumentConverter
                converter = DocumentConverter()
                metadata = {"title": title}
                markdown_text = converter.to_markdown(content, metadata)
                file_path = os.path.join(base_path, f"{safe_title}.md")
                self._save_markdown(file_path, markdown_text)
                self.logger.info(f"{'  ' * level}✅ 已保存MD: {safe_title}.md")
                exported_any = True
            else:
                self.logger.warning(f"{'  ' * level}⚠️ 无法导出Markdown（获取内容失败）")
        
        # Word和PDF使用飞书原生API导出
        native_formats = [fmt for fmt in self.export_formats if fmt in ['docx', 'pdf']]
        
        if native_formats:
            from feishu_native_exporter import FeishuNativeExporter
            exporter = FeishuNativeExporter(self.api)
            
            export_token = obj_token if obj_token else node_token
            export_type = obj_type if obj_type else (node_type or "docx")
            
            # 批量导出
            os.makedirs(base_path, exist_ok=True)
            results = exporter.export_document_batch(
                export_token, 
                export_type, 
                native_formats, 
                base_path, 
                safe_title
            )
            
            for fmt, (success, error) in results.items():
                if success:
                    self.logger.info(f"{'  ' * level}✅ 已保存{fmt.upper()} (原生): {safe_title}.{fmt}")
                    exported_any = True
                else:
                    self.logger.warning(f"{'  ' * level}⚠️ 导出{fmt.upper()}失败: {error}")
        
        return 1 if exported_any else 0
    
    def _process_node_parallel(self, node: Dict[str, Any], base_path: str, space_id: str, level: int = 0) -> int:
        """
        并行处理节点（核心优化）
        
        Args:
            node: 节点信息
            base_path: 保存路径
            space_id: 空间ID
            level: 层级
            
        Returns:
            成功导出的文档数量
        """
        node_token = node.get("node_token")
        title = node.get("title", "未命名")
        has_child = node.get("has_child", False)
        
        # 避免重复
        if node_token in self.crawled_nodes:
            return 0
        self.crawled_nodes.add(node_token)
        
        count = 0
        
        # 处理当前文档（如果是文档类型）
        node_type = node.get("node_type")
        obj_type = node.get("obj_type", "")
        
        if node_type in ["doc", "docx"] or obj_type in ["doc", "docx"]:
            # 使用父类的单文档处理方法
            count += self._process_single_node(node, base_path, level)
        
        # 🚀 并行处理子节点（关键优化）
        if has_child:
            self.logger.info(f"{'  ' * level}📁 进入目录: {title}")
            
            # 创建子目录
            safe_title = self._sanitize_filename(title)
            sub_dir = os.path.join(base_path, safe_title)
            os.makedirs(sub_dir, exist_ok=True)
            
            # 获取子节点
            child_nodes = self.get_child_nodes(space_id, node_token)
            
            if child_nodes:
                # ⚡ 使用线程池并行处理子节点
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    # 提交所有子节点任务
                    future_to_node = {
                        executor.submit(
                            self._process_node_parallel, 
                            child, 
                            sub_dir, 
                            space_id, 
                            level + 1
                        ): child 
                        for child in child_nodes
                    }
                    
                    # 收集结果
                    for future in as_completed(future_to_node):
                        try:
                            child_count = future.result()
                            count += child_count
                        except Exception as e:
                            child = future_to_node[future]
                            self.logger.error(f"处理节点失败 {child.get('title')}: {str(e)}")
        
        return count
    
    def crawl_wiki(self, wiki_link: str, save_path: str) -> tuple:
        """
        并行爬取Wiki（覆盖父类方法）
        
        Args:
            wiki_link: Wiki链接
            save_path: 保存路径
            
        Returns:
            (成功数量, 错误信息)
        """
        try:
            # 提取space_id
            space_id = self.extract_space_id_from_link(wiki_link)
            if not space_id:
                return (0, "无法从链接中提取space_id")
            
            self.logger.info(f"开始并行爬取Wiki: {space_id}")
            self.logger.info(f"并行数: {self.max_workers} 个文档同时处理")
            
            # 获取根节点
            root_nodes = self.get_child_nodes(space_id, None)
            if not root_nodes:
                return (0, "无法获取Wiki根节点")
            
            # 创建保存目录
            import time
            output_dir = os.path.join(save_path, f"Wiki导出_{int(time.time())}")
            os.makedirs(output_dir, exist_ok=True)
            
            total_count = 0
            
            # 🚀 并行处理所有根节点
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_node = {
                    executor.submit(
                        self._process_node_parallel,
                        node,
                        output_dir,
                        space_id,
                        0
                    ): node
                    for node in root_nodes
                }
                
                for i, future in enumerate(as_completed(future_to_node), 1):
                    try:
                        node = future_to_node[future]
                        count = future.result()
                        total_count += count
                        self.logger.info(f"[{i}/{len(root_nodes)}] 完成: {node.get('title')} ({count}篇)")
                    except Exception as e:
                        node = future_to_node[future]
                        self.logger.error(f"处理根节点失败 {node.get('title')}: {str(e)}")
            
            self.logger.info(f"🎉 爬取完成！共导出 {total_count} 篇文档")
            self.logger.info(f"📂 保存位置: {output_dir}")
            
            return (total_count, "")
            
        except Exception as e:
            error_msg = f"批量爬取失败: {str(e)}"
            self.logger.error(error_msg)
            import traceback
            traceback.print_exc()
            return (0, error_msg)
