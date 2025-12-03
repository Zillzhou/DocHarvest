"""
Markdown转换模块
将飞书文档内容转换为Markdown格式
"""
import re
import logging
from typing import Dict, Any, List


class MarkdownConverter:
    """飞书文档到Markdown转换器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, doc_content: Dict[str, Any], doc_metadata: Dict[str, Any] = None) -> str:
        """
        将飞书文档内容转换为Markdown
        
        Args:
            doc_content: 文档内容（从API获取的原始内容）
            doc_metadata: 文档元数据（可选）
            
        Returns:
            Markdown格式的字符串
        """
        if not doc_content:
            self.logger.error("文档内容为空")
            return ""
        
        markdown_lines = []
        
        # 添加文档标题
        if doc_metadata and doc_metadata.get("title"):
            title = doc_metadata.get("title", "未命名文档")
            markdown_lines.append(f"# {title}\n")
        
        # 获取纯文本内容
        content = doc_content.get("content", "")
        
        if content:
            # 飞书的raw_content API返回的是纯文本
            # 我们进行简单的格式化处理
            markdown_lines.append(self._format_content(content))
        else:
            self.logger.warning("文档内容为空")
            markdown_lines.append("*文档内容为空*")
        
        return "\n".join(markdown_lines)
    
    def _format_content(self, content: str) -> str:
        """
        格式化内容
        
        Args:
            content: 原始文本内容
            
        Returns:
            格式化后的内容
        """
        # 清理多余的空行
        lines = content.split('\n')
        formatted_lines = []
        
        prev_empty = False
        for line in lines:
            stripped = line.strip()
            
            # 跳过连续的空行
            if not stripped:
                if not prev_empty:
                    formatted_lines.append("")
                    prev_empty = True
                continue
            
            prev_empty = False
            
            # 检测可能的标题（基于缩进和内容）
            if self._is_likely_heading(stripped, line):
                # 根据上下文判断标题级别
                level = self._detect_heading_level(stripped)
                formatted_lines.append(f"{'#' * level} {stripped}")
            else:
                formatted_lines.append(line)
        
        return "\n".join(formatted_lines)
    
    def _is_likely_heading(self, stripped: str, original: str) -> bool:
        """
        判断一行文本是否可能是标题
        
        Args:
            stripped: 去除空格后的文本
            original: 原始文本
            
        Returns:
            是否可能是标题
        """
        # 标题特征：
        # 1. 相对较短（通常少于50个字符）
        # 2. 不以标点符号结尾
        # 3. 可能包含数字编号
        
        if len(stripped) > 80:
            return False
        
        # 如果以数字编号开头，可能是标题
        if re.match(r'^[\d一二三四五六七八九十]+[、\.\s]', stripped):
            return True
        
        # 如果全是大写字母或中文，且较短，可能是标题
        if len(stripped) < 30 and not stripped.endswith(('。', '，', ',', '.', '；', ';')):
            return True
        
        return False
    
    def _detect_heading_level(self, text: str) -> int:
        """
        检测标题级别
        
        Args:
            text: 文本内容
            
        Returns:
            标题级别（1-6）
        """
        # 根据编号前缀判断级别
        if re.match(r'^一[、\.]', text) or re.match(r'^1[、\.]', text):
            return 2
        elif re.match(r'^[\d一二三四五六七八九十]+[、\.]', text):
            return 3
        elif len(text) < 20:
            return 2
        else:
            return 3
    
    def convert_simple(self, raw_text: str, title: str = "") -> str:
        """
        简单转换：直接将纯文本转换为Markdown
        
        Args:
            raw_text: 原始文本
            title: 文档标题
            
        Returns:
            Markdown格式文本
        """
        markdown_lines = []
        
        if title:
            markdown_lines.append(f"# {title}\n")
        
        # 保持原始格式，只做基本清理
        cleaned_text = raw_text.strip()
        markdown_lines.append(cleaned_text)
        
        return "\n".join(markdown_lines)

