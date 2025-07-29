# -- coding: utf-8 --
# Project: object_storage
# Created Date: 2025-05-01
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

import os
import logging
from typing import List, Optional
import oss2
from ..object_storage import ObjectStorage, StorageConfig

logger = logging.getLogger(__name__)

# 设置oss2的日志级别为WARNING，关闭INFO级别的日志
oss2.set_stream_logger(level=logging.WARNING)

class AliCloudStorage(ObjectStorage):
    """阿里云OSS存储实现"""
    
    def __init__(self, config: StorageConfig):
        """初始化阿里云OSS客户端
        
        Args:
            config: 存储配置对象
        """
        super().__init__(config)
        self.auth = oss2.Auth(config.access_key, config.secret_key)
        self.bucket = oss2.Bucket(
            auth=self.auth,
            endpoint=config.endpoint,
            bucket_name=config.bucket_name
        )
        
    def upload_file(self, object_key: str, data: bytes) -> bool:
        """上传文件到阿里云OSS
        
        Args:
            object_key: 对象存储中的key
            data: 文件数据
        Returns:
            bool: 是否上传成功
        """
        try:
            self.bucket.put_object(object_key, data)
            logger.info(f"文件上传成功: {object_key}")
            return True
        except Exception as e:
            logger.error(f"文件上传失败: {str(e)}")
            return False
            
    def download_file(self, object_key: str) -> bytes:
        """从阿里云OSS下载文件
        
        Args:
            object_key: 对象存储中的key
            
        Returns:
            bytes: 文件内容
        """
        try:
            return self.bucket.get_object(object_key).read()
        except Exception as e:
            logger.error(f"文件下载失败: {str(e)}")
            return None
            
    def delete_file(self, object_key: str) -> bool:
        """删除阿里云OSS中的文件
        
        Args:
            object_key: 对象存储中的key
            
        Returns:
            bool: 是否删除成功
        """
        try:
            self.bucket.delete_object(object_key)
            logger.info(f"文件删除成功: {object_key}")
            return True
        except Exception as e:
            logger.error(f"文件删除失败: {str(e)}")
            return False
            
    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """列出阿里云OSS中的文件
        
        Args:
            prefix: 文件前缀过滤
            
        Returns:
            List[str]: 文件key列表
        """
        try:
            files = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
                files.append(obj.key)
            return files
        except Exception as e:
            logger.error(f"列出文件失败: {str(e)}")
            return [] 