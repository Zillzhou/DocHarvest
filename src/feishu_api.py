"""
飞书API处理模块
负责与飞书开放平台API交互
"""
import requests
import json
import re
from typing import Optional, Dict, Any
import logging


class FeishuAPI:
    """飞书API客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化飞书API客户端
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.base_url = "https://open.feishu.cn/open-apis"
        
        # 配置日志
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, method: str, url: str, headers: dict = None, 
                     params: dict = None, json_data: dict = None, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """
        通用HTTP请求方法
        
        Args:
            method: 请求方法 (GET, POST等)
            url: 请求URL
            headers: 请求头
            params: URL参数
            json_data: JSON数据
            timeout: 超时时间
            
        Returns:
            响应JSON或None
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"HTTP请求失败: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"请求异常: {str(e)}")
            return None
    
    def get_tenant_access_token(self) -> Optional[str]:
        """
        获取tenant_access_token
        
        Returns:
            access_token字符串，失败返回None
        """
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            self.logger.info("正在获取access_token...")
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") == 0:
                self.access_token = result.get("tenant_access_token")
                self.logger.info("成功获取access_token")
                return self.access_token
            else:
                self.logger.error(f"获取access_token失败: {result.get('msg')}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"网络请求失败: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"未知错误: {str(e)}")
            return None
    
    def extract_document_id(self, share_link: str) -> Optional[str]:
        """
        从飞书分享链接中提取文档ID
        
        支持的链接格式：
        - https://example.feishu.cn/docx/xxxxx
        - https://example.feishu.cn/docs/xxxxx
        - https://example.feishu.cn/wiki/xxxxx
        
        Args:
            share_link: 飞书文档分享链接
            
        Returns:
            文档ID，失败返回None
        """
        # 匹配各种飞书文档链接格式
        patterns = [
            r'feishu\.cn/docx/([a-zA-Z0-9_-]+)',
            r'feishu\.cn/docs/([a-zA-Z0-9_-]+)',
            r'feishu\.cn/wiki/([a-zA-Z0-9_-]+)',
            r'feishu\.cn/document/([a-zA-Z0-9_-]+)',
            r'larksuite\.com/docx/([a-zA-Z0-9_-]+)',
            r'larksuite\.com/docs/([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, share_link)
            if match:
                doc_id = match.group(1)
                self.logger.info(f"提取到文档ID: {doc_id}")
                return doc_id
        
        self.logger.error("无法从链接中提取文档ID")
        return None
    
    def get_document_content(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文档原始内容
        
        Args:
            document_id: 文档ID
            
        Returns:
            文档内容字典，失败返回None
        """
        if not self.access_token:
            self.logger.error("请先获取access_token")
            return None
        
        url = f"{self.base_url}/docx/v1/documents/{document_id}/raw_content"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        try:
            self.logger.info(f"正在获取文档内容: {document_id}")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") == 0:
                self.logger.info("成功获取文档内容")
                return result.get("data")
            else:
                self.logger.error(f"获取文档内容失败: {result.get('msg')}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"网络请求失败: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"未知错误: {str(e)}")
            return None
    
    def get_document_metadata(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文档元数据（标题等信息）
        
        Args:
            document_id: 文档ID
            
        Returns:
            文档元数据，失败返回None
        """
        if not self.access_token:
            self.logger.error("请先获取access_token")
            return None
        
        url = f"{self.base_url}/docx/v1/documents/{document_id}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        try:
            self.logger.info(f"正在获取文档元数据: {document_id}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") == 0:
                self.logger.info("成功获取文档元数据")
                return result.get("data", {}).get("document", {})
            else:
                self.logger.error(f"获取文档元数据失败: {result.get('msg')}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"网络请求失败: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"未知错误: {str(e)}")
            return None

