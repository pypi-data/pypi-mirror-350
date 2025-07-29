# -- coding: utf-8 --
# Project: object_storage
# Created Date: 2025-05-01
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from io import BytesIO
import logging
from typing import List, Optional
from minio import Minio
from minio.error import S3Error
from ..object_storage import ObjectStorage, StorageConfig

logger = logging.getLogger(__name__)

class MinioStorage(ObjectStorage):
    """MinIO存储实现"""
    
    def __init__(self, config: StorageConfig):
        """初始化MinIO客户端
        
        Args:
            config: 存储配置对象
        """
        super().__init__(config)
        
        # 处理endpoint格式
        endpoint = self._format_endpoint(config.endpoint)
        
        self.client = Minio(
            endpoint=endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=config.use_https  # 是否使用HTTPS
        )
        self.bucket_name = config.bucket_name
        
        # 确保bucket存在
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            logger.info(f"创建bucket: {self.bucket_name}")
        
    def _format_endpoint(self, endpoint: str) -> str:
        """格式化endpoint，确保符合MinIO要求
        
        Args:
            endpoint: 原始endpoint
            
        Returns:
            str: 格式化后的endpoint
            
        Raises:
            ValueError: endpoint格式不正确
        """
        # 移除协议前缀
        if endpoint.startswith(('http://', 'https://')):
            endpoint = endpoint.split('://', 1)[1]
            
        # 移除路径部分
        endpoint = endpoint.split('/', 1)[0]
        
        # 验证格式
        if '/' in endpoint:
            raise ValueError("MinIO endpoint不能包含路径，格式应为: host:port")
            
        return endpoint
        
    def upload_file(self, object_key: str, data: bytes) -> bool:
        """上传文件到MinIO
        
        Args:
            object_key: 对象存储中的key
            data: 文件数据
            
        Returns:
            bool: 是否上传成功
        """
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
                data=BytesIO(data),
                length=len(data)
            )
            logger.info(f"文件上传成功: {object_key}")
            return True
        except S3Error as e:
            logger.error(f"文件上传失败: {str(e)}")
            return False
            
    def download_file(self, object_key: str) -> bytes:
        """从MinIO下载文件
        
        Args:
            object_key: 对象存储中的key
            
        Returns:
            bytes: 文件内容
        """
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=object_key
            )
            return response.read()
        except S3Error as e:
            logger.error(f"文件下载失败: {str(e)}")
            return None
            
    def delete_file(self, object_key: str) -> bool:
        """删除MinIO中的文件
        
        Args:
            object_key: 对象存储中的key
            
        Returns:
            bool: 是否删除成功
        """
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_key
            )
            logger.info(f"文件删除成功: {object_key}")
            return True
        except S3Error as e:
            logger.error(f"文件删除失败: {str(e)}")
            return False
            
    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """列出MinIO中的文件
        
        Args:
            prefix: 文件前缀过滤
            
        Returns:
            List[str]: 文件key列表
        """
        try:
            files = []
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix
            )
            for obj in objects:
                files.append(obj.object_name)
            return files
        except S3Error as e:
            logger.error(f"列出文件失败: {str(e)}")
            return [] 