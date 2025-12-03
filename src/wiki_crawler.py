"""
Wiki批量爬取模块
支持自动递归获取Wiki的所有子页面
"""
import os
import re
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from feishu_api import FeishuAPI


class WikiCrawler:
    """Wiki批量爬取器"""
    
    def __init__(self, api: FeishuAPI, export_formats: List[str] = None):
        """
        初始化Wiki爬取器
        
        Args:
            api: FeishuAPI实例
            export_formats: 导出格式列表，如 ['md', 'docx', 'pdf']
        """
        self.api = api
        self.logger = logging.getLogger(__name__)
        self.crawled_nodes = set()  # 记录已爬取的节点，避免重复
        self.export_formats = export_formats or ['md']
    
    def extract_space_id_from_link(self, wiki_link: str) -> Optional[str]:
        """
        从Wiki链接中提取space_id
        
        支持的链接格式：
        1. https://xxx.feishu.cn/wiki/space/7349729703127482369?xxx (分享链接，推荐)
        2. https://xxx.feishu.cn/wiki/space/7349729703127482369/wiki/xxx
        3. https://xxx.feishu.cn/wiki/ZFKlW6SLei2vLDkZXu3cS0BSn9c (wiki token)
        
        Args:
            wiki_link: Wiki链接
            
        Returns:
            space_id 或 wiki_token
        """
        # 模式1: 直接包含数字space_id（分享知识库链接）
        # /wiki/space/7349729703127482369
        pattern1 = r'feishu\.cn/wiki/space/(\d+)'
        match1 = re.search(pattern1, wiki_link)
        
        if match1:
            space_id = match1.group(1)
            self.logger.info(f"✅ 直接提取到space_id: {space_id}")
            return space_id
        
        # 模式2: 包含space路径和wiki token
        # /wiki/space/xxx/wiki/token
        pattern2 = r'feishu\.cn/wiki/space/[^/]+/wiki/([a-zA-Z0-9_-]+)'
        match2 = re.search(pattern2, wiki_link)
        
        if match2:
            wiki_token = match2.group(1)
            self.logger.info(f"提取到Wiki token: {wiki_token}")
            return wiki_token
        
        # 模式3: 直接wiki token
        pattern3 = r'feishu\.cn/wiki/([a-zA-Z0-9_-]+)'
        match3 = re.search(pattern3, wiki_link)
        
        if match3:
            wiki_token = match3.group(1)
            self.logger.info(f"提取到Wiki token: {wiki_token}")
            return wiki_token
        
        self.logger.error("无法从链接中提取space_id或wiki_token")
        return None
    
    def get_wiki_space_info(self, wiki_token: str) -> Optional[str]:
        """
        通过wiki_token获取space_id
        
        Args:
            wiki_token: Wiki token
            
        Returns:
            space_id 或 None
        """
        if not self.api.access_token:
            self.logger.error("请先获取access_token")
            return None
        
        # 使用wiki/v2/spaces接口获取space信息
        url = f"{self.api.base_url}/wiki/v2/spaces/{wiki_token}"
        
        headers = {
            "Authorization": f"Bearer {self.api.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        try:
            self.logger.info(f"正在获取Wiki space信息: {wiki_token}")
            response = self.api._make_request('GET', url, headers=headers)
            
            if response and response.get("code") == 0:
                space = response.get("data", {}).get("space", {})
                space_id = space.get("space_id")
                if space_id:
                    self.logger.info(f"成功获取space_id: {space_id}")
                    return space_id
                else:
                    self.logger.error("响应中没有space_id")
                    return None
            else:
                error_msg = response.get('msg', 'Unknown error') if response else 'No response'
                self.logger.error(f"获取space信息失败: {error_msg}")
                return None
                
        except Exception as e:
            self.logger.error(f"获取space信息异常: {str(e)}")
            return None
    
    def get_child_nodes(self, space_id: str, parent_node_token: str = None) -> List[Dict[str, Any]]:
        """
        获取子节点列表
        
        Args:
            space_id: 知识空间ID
            parent_node_token: 父节点token，为None时获取根节点
            
        Returns:
            子节点列表
        """
        if not self.api.access_token:
            self.logger.error("请先获取access_token")
            return []
        
        url = f"{self.api.base_url}/wiki/v2/spaces/{space_id}/nodes"
        
        headers = {
            "Authorization": f"Bearer {self.api.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        params = {
            "page_size": 50
        }
        
        if parent_node_token:
            params["parent_node_token"] = parent_node_token
        
        all_nodes = []
        page_token = None
        
        try:
            while True:
                if page_token:
                    params["page_token"] = page_token
                
                self.logger.info(f"正在获取子节点列表: parent={parent_node_token or 'root'}")
                response = self.api._make_request('GET', url, headers=headers, params=params)
                
                if not response or response.get("code") != 0:
                    self.logger.error(f"获取子节点失败: {response.get('msg') if response else 'No response'}")
                    break
                
                data = response.get("data", {})
                items = data.get("items", [])
                all_nodes.extend(items)
                
                # 检查是否还有更多页
                page_token = data.get("page_token")
                if not data.get("has_more", False):
                    break
                
                time.sleep(0.5)  # 避免请求过快
            
            self.logger.info(f"获取到 {len(all_nodes)} 个子节点")
            return all_nodes
            
        except Exception as e:
            self.logger.error(f"获取子节点异常: {str(e)}")
            return []
    
    def crawl_node(self, node: Dict[str, Any], base_path: str, space_id: str, level: int = 0) -> int:
        """
        递归爬取节点及其子节点
        
        Args:
            node: 节点信息
            base_path: 保存基础路径
            space_id: Wiki空间ID
            level: 当前层级
            
        Returns:
            爬取的文档数量
        """
        node_token = node.get("node_token")
        node_type = node.get("node_type")  # doc, docx, sheet, etc.
        obj_type = node.get("obj_type", "")  # 对象类型
        obj_token = node.get("obj_token", "")  # 对象token (用于导出API)
        title = node.get("title", "未命名")
        has_child = node.get("has_child", False)
        
        # 避免重复爬取
        if node_token in self.crawled_nodes:
            self.logger.info(f"节点已爬取，跳过: {title}")
            return 0
        
        self.crawled_nodes.add(node_token)
        count = 0
        
        # 清理文件名
        safe_title = self._sanitize_filename(title)
        
        # 如果是文档类型，下载内容
        # node_type可能是空的，也可以检查obj_type
        if node_type in ["doc", "docx"] or obj_type in ["doc", "docx"]:
            self.logger.info(f"{'  ' * level}📄 爬取文档: {title}")
            
            # 标记是否成功导出了至少一种格式
            exported_any = False
            
            # 获取文档内容（仅用于Markdown导出）
            # 注意：旧版文档（doc）可能无法获取内容，但仍可以导出PDF/Word
            content = None
            if 'md' in self.export_formats:
                content = self.api.get_document_content(node_token)
            
            # Markdown需要文档内容
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
            
            # Word和PDF使用飞书原生API导出（不需要预先获取内容）
            native_formats = [fmt for fmt in self.export_formats if fmt in ['docx', 'pdf']]
            
            if native_formats:
                from feishu_native_exporter import FeishuNativeExporter
                exporter = FeishuNativeExporter(self.api)
                
                # 使用obj_token进行导出（这是Wiki节点对应的文档token）
                export_token = obj_token if obj_token else node_token
                export_type = obj_type if obj_type else (node_type or "docx")
                
                # 🚀 批量导出（并行处理）- 同时创建所有任务
                os.makedirs(base_path, exist_ok=True)
                results = exporter.export_document_batch(
                    export_token, 
                    export_type, 
                    native_formats, 
                    base_path, 
                    safe_title
                )
                
                # 处理结果
                for fmt, (success, error) in results.items():
                    if success:
                        self.logger.info(f"{'  ' * level}✅ 已保存{fmt.upper()} (原生): {safe_title}.{fmt}")
                        exported_any = True
                    else:
                        self.logger.warning(f"{'  ' * level}⚠️ 导出{fmt.upper()}失败: {error}")
            
            # 如果成功导出了任何格式，计数+1
            if exported_any:
                count += 1
            else:
                self.logger.warning(f"{'  ' * level}⚠️ 所有格式导出失败: {title}")
        
        # 如果有子节点，递归爬取
        if has_child:
            self.logger.info(f"{'  ' * level}📁 进入目录: {title}")
            
            # 创建子目录
            sub_dir = os.path.join(base_path, safe_title)
            os.makedirs(sub_dir, exist_ok=True)
            
            # 获取子节点
            child_nodes = self.get_child_nodes(space_id, node_token)
            
            # 递归爬取每个子节点
            for child in child_nodes:
                count += self.crawl_node(child, sub_dir, space_id, level + 1)
                time.sleep(0.5)  # 避免请求过快
        
        return count
    
    def crawl_wiki(self, wiki_link: str, save_path: str, progress_callback=None) -> Tuple[int, str]:
        """
        爬取整个Wiki
        
        Args:
            wiki_link: Wiki链接
            save_path: 保存路径
            progress_callback: 进度回调函数 callback(message)
            
        Returns:
            (成功数量, 错误信息)
        """
        def log_progress(msg):
            self.logger.info(msg)
            if progress_callback:
                progress_callback(msg)
        
        try:
            # 提取space_id或wiki_token
            log_progress("📋 正在解析Wiki链接...")
            space_id = self.extract_space_id_from_link(wiki_link)
            
            if not space_id:
                return (0, "无法解析Wiki链接，请确认链接格式正确")
            
            # 判断是space_id还是wiki_token
            if space_id.isdigit():
                # 已经是space_id（纯数字），直接使用
                log_progress(f"✅ Space ID: {space_id} (从链接直接获取)")
            else:
                # 是wiki_token，需要通过API获取space_id
                log_progress(f"📝 Wiki Token: {space_id}")
                log_progress("🔍 正在通过Token获取Space ID...")
                wiki_token = space_id
                space_id = self.get_wiki_space_info(wiki_token)
                
                if not space_id:
                    return (0, "无法获取Wiki空间ID，可能是权限不足或Wiki不存在")
                
                log_progress(f"✅ Space ID: {space_id}")
            
            # 创建输出目录
            output_dir = os.path.join(save_path, f"Wiki导出_{int(time.time())}")
            os.makedirs(output_dir, exist_ok=True)
            log_progress(f"📁 输出目录: {output_dir}")
            
            # 获取根节点列表（不指定parent_node_token获取所有根节点）
            log_progress("📥 正在获取文档列表...")
            root_nodes = self.get_child_nodes(space_id, None)
            
            if not root_nodes:
                return (0, "未找到任何文档。可能原因：\n1. 该Wiki为空\n2. 权限不足\n3. Space ID不正确")
            
            log_progress(f"📊 找到 {len(root_nodes)} 个根节点")
            
            # 递归爬取所有节点
            log_progress("🚀 开始批量爬取...")
            self.crawled_nodes.clear()  # 清空已爬取记录
            
            total_count = 0
            for i, node in enumerate(root_nodes, 1):
                title = node.get('title', 'Unknown')
                log_progress(f"[{i}/{len(root_nodes)}] 处理: {title}")
                count = self.crawl_node(node, output_dir, space_id, 0)
                total_count += count
                time.sleep(0.5)
            
            if total_count > 0:
                log_progress(f"🎉 爬取完成！共导出 {total_count} 篇文档")
                log_progress(f"📂 保存位置: {output_dir}")
                return (total_count, "")
            else:
                return (0, "没有成功导出任何文档，请检查权限和文档类型")
            
        except Exception as e:
            import traceback
            error_msg = f"爬取过程出错: {str(e)}"
            self.logger.error(traceback.format_exc())
            log_progress(f"❌ {error_msg}")
            return (0, error_msg)
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名中的非法字符"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 移除前后空格
        filename = filename.strip()
        
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename or "未命名"
    
    def _save_markdown(self, file_path: str, content: str):
        """保存Markdown文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.logger.error(f"保存文件失败 {file_path}: {str(e)}")

