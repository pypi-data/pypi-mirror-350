#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import uuid
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from typing import Dict, Any, Union, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("feishusdk")

# 全局客户端实例
_client = None

def init_bot(app_id=None, app_secret=None, config_file=None, log_level="INFO"):
    """
    初始化飞书机器人
    
    Args:
        app_id: 应用ID
        app_secret: 应用密钥
        config_file: 配置文件路径
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        初始化是否成功
    """
    global _client
    
    # 设置日志级别
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }
    logger.setLevel(level_map.get(log_level.upper(), logging.INFO))
    
    # 从配置文件加载
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                app_id = config.get('app_id') or app_id
                app_secret = config.get('app_secret') or app_secret
                logger.info(f"从配置文件加载凭证: {config_file}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            return False
    
    # 验证是否有必要的配置
    if not app_id or not app_secret:
        logger.error("必须提供app_id和app_secret")
        return False
    
    try:
        # 创建lark客户端
        _client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(_parse_lark_log_level(log_level)) \
            .build()
        
        logger.info(f"飞书机器人初始化成功，App ID: {app_id}")
        return True
    except Exception as e:
        logger.error(f"初始化飞书机器人失败: {str(e)}")
        return False

def _parse_lark_log_level(level_str):
    """将字符串日志级别转换为lark.LogLevel枚举值"""
    level_map = {
        "DEBUG": lark.LogLevel.DEBUG,
        "INFO": lark.LogLevel.INFO,
        "WARNING": lark.LogLevel.WARNING,
        "WARN": lark.LogLevel.WARNING,
        "ERROR": lark.LogLevel.ERROR
    }
    return level_map.get(level_str.upper(), lark.LogLevel.INFO)

class BotMessage:
    """
    飞书机器人消息发送类
    
    用法示例:
    message = BotMessage("chat_id", {"type": "text", "content": "Hello"})
    result = message.send()
    """
    
    def __init__(self, group_id, content):
        """
        初始化消息
        
        Args:
            group_id: 群组ID
            content: 消息内容，格式为 {"type": "xxx", "content": xxx}
                type可以是: text, post, interactive
                content根据type有不同的格式
        """
        self.group_id = group_id
        self.content = content
        self.msg_type = content.get("type", "text")
        self.msg_content = content.get("content", "")
    
    def send(self):
        """
        发送消息
        
        Returns:
            成功返回消息ID，失败返回None
        """
        global _client
        
        # 检查客户端是否初始化
        if _client is None:
            logger.error("飞书机器人未初始化，请先调用init_bot()")
            return None
        
        # 格式化消息内容
        formatted_content = self._format_content()
        
        logger.info(f"发送{self.msg_type}消息到群组: {self.group_id}")
        logger.debug(f"消息内容: {formatted_content}")
        
        try:
            # 构造请求对象
            request = CreateMessageRequest.builder() \
                .receive_id_type("chat_id") \
                .request_body(CreateMessageRequestBody.builder()
                    .receive_id(self.group_id)
                    .msg_type(self.msg_type)
                    .content(formatted_content)
                    .uuid(str(uuid.uuid4()))
                    .build()) \
                .build()
            
            # 发起请求
            response = _client.im.v1.message.create(request)
            
            # 处理失败返回
            if not response.success():
                error_msg = f"发送消息失败, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
                logger.error(error_msg)
                if hasattr(response, 'raw') and response.raw and hasattr(response.raw, 'content'):
                    logger.error(f"错误详情: {response.raw.content}")
                return None
            
            logger.info("消息发送成功")
            # 返回消息ID
            return response.data.message_id
            
        except Exception as e:
            logger.error(f"发送消息时发生错误: {str(e)}")
            return None
    
    def _format_content(self):
        """
        根据消息类型格式化内容
        
        Returns:
            格式化后的JSON字符串
        """
        content = self.msg_content
        msg_type = self.msg_type
        
        # 如果已经是字符串，确保它是有效的JSON
        if isinstance(content, str):
            try:
                # 尝试解析为JSON，确认格式正确
                json.loads(content)
                return content
            except:
                # 如果不是JSON字符串，则根据消息类型封装
                if msg_type == "text":
                    return json.dumps({"text": content})
                else:
                    # 对于其他类型，必须是有效的JSON结构
                    raise ValueError(f"消息类型为{msg_type}时，内容必须是有效的JSON结构")
        
        # 如果是字典，转换为JSON字符串
        if isinstance(content, dict):
            # 文本消息特殊处理
            if msg_type == "text":
                if "text" not in content:
                    return json.dumps({"text": json.dumps(content)})
            return json.dumps(content)
        
        # 其他情况，尝试转换为字符串
        return json.dumps({"text": str(content)})

def get_group_list(page_size=50):
    """
    获取机器人所在的群组列表
    
    Args:
        page_size: 每页数量
        
    Returns:
        群组列表，失败返回空列表
    """
    global _client
    
    # 检查客户端是否初始化
    if _client is None:
        logger.error("飞书机器人未初始化，请先调用init_bot()")
        return []
    
    chats = []
    page_token = None
    
    try:
        while True:
            # 构造请求
            request = ListChatRequest.builder() \
                .page_size(page_size)
            
            if page_token:
                request.page_token(page_token)
            
            request = request.build()
            
            # 发起请求
            response = _client.im.v1.chat.list(request)
            
            # 处理失败返回
            if not response.success():
                error_msg = f"获取群组列表失败, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
                logger.error(error_msg)
                return []
            
            # 添加结果
            items = response.data.items
            if items:
                chats.extend(items)
            
            # 处理分页
            if not response.data.has_more:
                break
                
            page_token = response.data.page_token
        
        logger.info(f"获取到 {len(chats)} 个群组")
        return chats
        
    except Exception as e:
        logger.error(f"获取群组列表时发生错误: {str(e)}")
        return []
