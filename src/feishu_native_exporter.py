"""
飞书原生PDF/Word导出模块
使用飞书官方API直接导出文档为PDF和Word格式
"""
import os
import time
import logging
import requests
from typing import Optional, Dict, Any, Tuple


class FeishuNativeExporter:
    """飞书原生导出器 - 使用官方API导出PDF/Word"""
    
    def __init__(self, api):
        """
        初始化导出器
        
        Args:
            api: FeishuAPI实例
        """
        self.api = api
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://open.feishu.cn/open-apis"
    
    def export_document_batch(self, doc_token: str, doc_type: str, export_formats: list, base_path: str, filename: str) -> Dict[str, Tuple[bool, str]]:
        """
        批量导出文档为多种格式（并行处理）
        
        Args:
            doc_token: 文档token
            doc_type: 文档类型
            export_formats: 导出格式列表，如 ['pdf', 'docx']
            base_path: 保存目录
            filename: 文件名（不含扩展名）
            
        Returns:
            字典 {格式: (是否成功, 错误信息)}
        """
        if not self.api.access_token:
            return {fmt: (False, "未获取access_token") for fmt in export_formats}
        
        results = {}
        tickets = {}
        
        # 步骤1: 并行创建所有导出任务
        for fmt in export_formats:
            self.logger.info(f"创建{fmt.upper()}导出任务: {doc_token}")
            ticket = self._create_export_task(doc_token, doc_type, fmt)
            if ticket:
                tickets[fmt] = ticket
            else:
                results[fmt] = (False, "创建任务失败")
        
        # 步骤2: 并行查询和下载所有任务
        for fmt, ticket in tickets.items():
            try:
                self.logger.info(f"查询{fmt.upper()}导出任务: {ticket}")
                file_token = self._query_export_result(ticket, doc_token)
                
                if not file_token:
                    results[fmt] = (False, "查询任务失败或超时")
                    continue
                
                # 下载文件
                save_path = os.path.join(base_path, f"{filename}.{fmt}")
                self.logger.info(f"下载{fmt.upper()}文件: {file_token}")
                success = self._download_exported_file(file_token, save_path)
                
                if success:
                    results[fmt] = (True, "")
                else:
                    results[fmt] = (False, "下载失败")
            except Exception as e:
                results[fmt] = (False, str(e))
        
        return results
    
    def export_document(self, doc_token: str, doc_type: str, export_format: str, save_path: str) -> Tuple[bool, str]:
        """
        导出文档为指定格式
        
        Args:
            doc_token: 文档token
            doc_type: 文档类型 ("doc", "docx", "sheet", "bitable")
            export_format: 导出格式 ("pdf", "docx", "xlsx")
            save_path: 保存路径
            
        Returns:
            (是否成功, 错误信息)
        """
        if not self.api.access_token:
            return False, "未获取access_token"
        
        try:
            # 步骤1: 创建导出任务
            self.logger.info(f"创建导出任务: {doc_token} -> {export_format}")
            ticket = self._create_export_task(doc_token, doc_type, export_format)
            if not ticket:
                return False, "创建导出任务失败"
            
            # 步骤2: 轮询查询任务结果（需要传入doc_token）
            self.logger.info(f"查询导出任务: {ticket}")
            file_token = self._query_export_result(ticket, doc_token)
            
            # 如果file_token为空，尝试直接使用ticket下载
            if not file_token:
                self.logger.warning(f"file_token为空，尝试使用ticket下载: {ticket}")
                file_token = ticket
            
            if not file_token:
                return False, "查询导出任务失败或超时"
            
            # 步骤3: 下载文件
            self.logger.info(f"下载导出文件: {file_token}")
            success = self._download_exported_file(file_token, save_path)
            if success:
                return True, ""
            else:
                return False, "下载文件失败"
                
        except Exception as e:
            self.logger.error(f"导出异常: {str(e)}")
            return False, str(e)
    
    def _create_export_task(self, doc_token: str, doc_type: str, export_format: str, retry_count: int = 2) -> Optional[str]:
        """
        创建导出任务（带重试）
        
        Args:
            doc_token: 文档token
            doc_type: 文档类型 (doc, docx, sheet等)
            export_format: 导出格式 (pdf, docx, xlsx等)
            retry_count: 重试次数
            
        Returns:
            任务ticket，失败返回None
        """
        url = f"{self.base_url}/drive/v1/export_tasks"
        
        headers = {
            "Authorization": f"Bearer {self.api.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 文档类型映射
        type_mapping = {
            "doc": "doc",
            "docx": "docx", 
            "sheet": "sheet",
            "bitable": "bitable"
        }
        
        payload = {
            "file_extension": export_format,  # pdf, docx, xlsx等
            "token": doc_token,
            "type": type_mapping.get(doc_type, "docx")
        }
        
        for attempt in range(retry_count + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                result = response.json()
                
                if result.get("code") == 0:
                    ticket = result.get("data", {}).get("ticket")
                    self.logger.info(f"导出任务已创建: {ticket}")
                    return ticket
                else:
                    error_msg = result.get('msg', 'Unknown error')
                    error_code = result.get('code')
                    self.logger.error(f"创建导出任务失败: code={error_code}, msg={error_msg}")
                    self.logger.error(f"请求参数: {payload}")
                    return None
                    
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                # 网络错误，可以重试
                if attempt < retry_count:
                    self.logger.warning(f"网络错误，{2}秒后重试 ({attempt + 1}/{retry_count}): {str(e)}")
                    time.sleep(2)
                    continue
                else:
                    self.logger.error(f"创建导出任务网络错误（已重试{retry_count}次）: {str(e)}")
                    self.logger.error(f"请求参数: {payload}")
                    return None
                    
            except requests.HTTPError as e:
                # HTTP错误，不重试
                error_detail = ""
                try:
                    error_detail = e.response.text
                    self.logger.error(f"HTTP错误详情: {error_detail}")
                except:
                    pass
                self.logger.error(f"创建导出任务HTTP错误: {str(e)}")
                self.logger.error(f"请求参数: {payload}")
                return None
            except Exception as e:
                self.logger.error(f"创建导出任务异常: {str(e)}")
                self.logger.error(f"请求参数: {payload}")
                return None
        
        return None
    
    def _query_export_result(self, ticket: str, doc_token: str, max_wait: int = 60) -> Optional[str]:
        """
        查询导出任务结果（带轮询）
        
        Args:
            ticket: 任务ID
            doc_token: 文档token（查询时必需）
            max_wait: 最大等待时间（秒）
            
        Returns:
            file_token 或 None
        """
        url = f"{self.base_url}/drive/v1/export_tasks/{ticket}"
        
        headers = {
            "Authorization": f"Bearer {self.api.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 查询参数：需要传入原始文档token
        params = {
            "token": doc_token
        }
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=20)
                response.raise_for_status()
                result = response.json()
                
                if result.get("code") == 0:
                    data = result.get("data", {})
                    
                    # API可能返回两种结构：data.result.xxx 或 data.xxx
                    result_data = data.get("result", data)
                    
                    # 检查任务状态
                    # 状态值: 0=成功, 2=进行中, 3=失败
                    job_status = result_data.get("job_status")
                    
                    is_success = (job_status == 0 or job_status == "success")
                    is_failed = (job_status == 3 or job_status == "failed")
                    
                    if is_success:  # 成功
                        # file_token可能在不同位置
                        file_token = (result_data.get("file_token") or 
                                     result_data.get("token") or
                                     result_data.get("ticket"))
                        
                        # 去除空字符串
                        if file_token:
                            file_token = file_token.strip()
                        
                        # 如果file_token有效，返回
                        if file_token:
                            self.logger.info(f"导出任务成功")
                            return file_token
                        else:
                            # 任务状态成功但file_token为空，继续等待
                            time.sleep(1)
                    elif is_failed:  # 失败
                        error_msg = data.get("job_error_msg", "Unknown error")
                        self.logger.error(f"导出任务失败: {error_msg}")
                        return None
                    else:  # 进行中，继续等待
                        # 🚀 优化：渐进式轮询间隔
                        check_count += 1
                        if check_count <= 3:
                            time.sleep(0.5)  # 前3次极速检查（小文档）
                        elif check_count <= 6:
                            time.sleep(1)    # 4-6次快速检查（中等文档）
                        else:
                            time.sleep(2)    # 之后正常间隔（大文档）
                else:
                    error_msg = result.get('msg', 'Unknown error')
                    error_code = result.get('code')
                    self.logger.error(f"查询导出任务失败: code={error_code}, msg={error_msg}")
                    return None
                    
            except (requests.exceptions.Timeout, requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
                # 网络超时或连接错误，等待后继续重试
                self.logger.warning(f"查询任务网络错误，2秒后重试: {str(e)}")
                time.sleep(2)
            except requests.HTTPError as e:
                # 捕获HTTP错误并打印响应内容
                error_detail = ""
                try:
                    error_detail = e.response.text
                    self.logger.error(f"查询任务HTTP错误详情: {error_detail}")
                except:
                    pass
                self.logger.error(f"查询导出任务HTTP错误: {str(e)}")
                time.sleep(2)
            except Exception as e:
                self.logger.warning(f"查询导出任务异常，继续重试: {str(e)}")
                time.sleep(2)
        
        self.logger.error("导出任务超时")
        return None
    
    def _download_exported_file(self, file_token: str, save_path: str) -> bool:
        """
        下载导出的文件
        
        Args:
            file_token: 文件token
            save_path: 保存路径
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/drive/v1/export_tasks/file/{file_token}/download"
        
        headers = {
            "Authorization": f"Bearer {self.api.access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 写入文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"文件已下载: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"下载文件异常: {str(e)}")
            return False
