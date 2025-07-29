"""
IM SDK Python封装模块

用于加载和封装Rust Universal IM SDK动态库
"""
import os
import ctypes
import sys
import threading
import time
from typing import Dict, Any, List

from native_mcp.imsdk import LIB_DIR
from native_mcp.imsdk.util import dict_to_ctypes,ctypes_to_dict
from native_mcp.lib import rcim_client
from native_mcp.lib.rcim_utils import string_cast, char_pointer_cast
from native_mcp.lib.rcim_client import (
    RcimConversationType_Group,
    RcimConversationType_Private,
    RcimDisconnectMode_NoPush,
    RcimEngineBuilder,
    RcimEngineBuilderParam,
    RcimEngineSync,
    RcimLogLevel_Debug,
    RcimMessageBox,
    RcimSendMessageOption
)

PLATFORM = rcim_client.RcimPlatform_Unknown
if sys.platform == 'darwin':
    PLATFORM = rcim_client.RcimPlatform_MacOS
elif sys.platform == 'win32':
    PLATFORM = rcim_client.RcimPlatform_Windows
elif sys.platform == 'linux':
    PLATFORM = rcim_client.RcimPlatform_Linux

USER_ID = ""

# 配置日志
from native_mcp.utils.mcp_utils import logger

class IMSDK:
    """IM SDK的Python封装类"""
    
    def __init__(self) -> None:
        """初始化IM SDK"""
        # 初始化属性
        self.engine = None
        self.builder = None
    
    def engine_build(self, app_key: str, navi_host: str, device_id: str) -> Dict[str, Any]:
        """
        初始化IM SDK并返回状态
        
        Args:
            app_key: 应用的AppKey
            device_id: 设备ID
            
        Returns:
            失败：包含code和message的字典
            成功：包含code、app_key、device_id和message的字典
        """
        if self.engine:
            return {"code": -1, "message": "引擎实例已经构建，请先调用destroy销毁引擎"}
        # 存储应用信息
        self.app_key = app_key
        self.device_id = device_id
        
        logger.info(f"初始化IM SDK，AppKey: {app_key}, 设备ID: {device_id}, 设备平台：{PLATFORM}")
        
        try:
            # 准备初始化参数
            engine_builder_param = {
                'app_key': app_key,
                "platform": PLATFORM,
                "device_id": device_id,
                "package_name": "",
                "imlib_version": "0.17.2",
                "device_model": "",
                "device_manufacturer": "",
                "os_version": "",
                "sdk_version_vec": {"name":"rust","version":"0.17.2"},
                "sdk_version_vec_len": 1,
                "app_version": "1.0.0",
            }
            
            # 创建参数结构体
            param = dict_to_ctypes(RcimEngineBuilderParam, engine_builder_param)
            
            # 创建builder指针
            builder = ctypes.pointer(ctypes.pointer(RcimEngineBuilder()))
            
            # 调用创建函数
            ret = rcim_client.rcim_create_engine_builder(param,builder)
            if ret != 0:
                logger.info(f"rcim_create_engine_builder failed, error code: {ret}")
                return {"code": -1, "message": f"rcim_create_engine_builder failed, error code: {ret}"}
            
            # 保存builder引用
            self.builder = builder.contents
            
            # 设置存储路径
            db_path = os.path.join(LIB_DIR, "rust_db")
            # 确保目录存在
            os.makedirs(db_path, exist_ok=True)
            
            ret = rcim_client.rcim_engine_builder_set_store_path(self.builder, char_pointer_cast(db_path))
            if ret != 0:
                logger.info(f"rcim_engine_builder_set_store_path failed, error code: {ret}")

            # 设置navi服务器
            navi_list = [navi_host]
            char_ptrs = (ctypes.POINTER(ctypes.c_char) * len(navi_list))()
            for i, string in enumerate(navi_list):
                if string is None:
                    char_ptrs[i] = None
                    continue
                # 创建对应字符串的 c_char 数组，并获取其指针
                char_array = ctypes.create_string_buffer(string.encode('utf-8'))
                char_ptrs[i] = ctypes.cast(char_array, ctypes.POINTER(ctypes.c_char))
            double_ptr = ctypes.cast(char_ptrs, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
            
            ret = rcim_client.rcim_engine_builder_set_navi_server(self.builder, double_ptr,1)
            if ret != 0:
                logger.info(f"rcim_engine_builder_set_navi_server failed, error code: {ret}")


            # 创建引擎
            engine_ptr = ctypes.pointer(ctypes.pointer(RcimEngineSync()))
            
            logger.info(f"rcim_engine_builder_build 即将执行")

            # 构建引擎
            ret = rcim_client.rcim_engine_builder_build(self.builder, engine_ptr)
            if ret != 0:
                logger.info(f"rcim_engine_builder_build failed, error code: {ret}")
                return {"code": -1, "message": f"rcim_engine_builder_build failed, error code: {ret}"}
            
            # 保存引擎引用
            self.engine = engine_ptr.contents

            rcim_client.rcim_engine_set_log_filter(self.engine,RcimLogLevel_Debug)

            return {
                "code": 0,
                "app_key": app_key,
                "device_id": device_id,
                "message": "IM SDK初始化成功"
            }
        except Exception as e:
            import traceback
            logger.info(f"初始化IM SDK失败: {e}")
            logger.info(f"异常堆栈: {traceback.format_exc()}")
            return {
                "code": -1,
                "message": str(e)
            }

    def engine_connect(self, token: str, timeout_sec: int = 10) -> Dict[str, Any]:
        """
        连接融云服务
        
        Args:
            token: 用户连接token
            timeout_sec: 连接超时时间，单位为秒
            
        Returns:
            失败：包含code和message的字典
            成功：包含code、user_id和message的字典
        """
        
        if not self.engine:
            return {"code": -1, "message": "引擎实例尚未构建，请先调用initialize初始化SDK"}
        
        logger.info(f"连接融云服务，token: {token}..., 超时: {timeout_sec}秒")
        
        # 创建回调数据类
        class ConnectData:
            def __init__(self):
                self.result = {"code": -1, "message": ""}
            
            def callback(self, user_data, code, user_id):

                logger.info(f"rcim_engine_connect 回调执行开始")
                # 从String类型获取字符串
                user_id_str = string_cast(user_id)
                # 将user_id_str赋值给全局变量_USER_ID
                global USER_ID
                USER_ID = user_id_str
                self.result = {
                    "code": code,
                    "user_id": user_id_str if code == 0 else "",
                    "message": "连接成功" if code == 0 else "连接失败"  
                }
                logger.info(f"连接回调: {'成功' if code == 0 else '失败'}, 用户ID: {user_id_str}, 错误码: {code}")
        
        # 创建回调数据
        callback_data = ConnectData()
        # 用事件等待回调完成
        connect_event = threading.Event()
        # 直接使用rcim_client模块中定义的RcimConnectCb类型
        # 创建回调函数
        def callback_wrapper(user_data, code, user_id):
            res = callback_data.callback(user_data, code, user_id)
            connect_event.set()
            return res
        
        # 使用正确的回调函数类型
        callback_fn = rcim_client.RcimConnectCb(callback_wrapper)
        
        # 正确地转换token
        token_buffer = char_pointer_cast(token)
        logger.info(f"token_buffer类型: {type(token)}")
        logger.info(f"token_buffer类型: {type(token_buffer)}")
        
        # 创建超时参数
        timeout_c = ctypes.c_int(timeout_sec)
        
        logger.info(f"rcim_engine_connect 即将执行")
        # 调用连接函数，注意引擎实例的访问方式
        rcim_client.rcim_engine_connect(
            self.engine[0],  # 使用self.engine[0]获取指针对象
            token_buffer,
            timeout_c,
            None,  # user_data参数设为None
            callback_fn
        )
        logger.info(f"rcim_engine_connect 执行完成")

        finished = connect_event.wait(timeout=timeout_sec + 1)
        if not finished:
            logger.info("连接超时，未收到回调")
            return {"code": -2, "message": "连接超时，未收到回调"}
        # 返回回调的结果
        return callback_data.result
    
    def send_message(self, receiver: str, content: str, conversation_type = RcimConversationType_Private) -> Dict[str, Any]:
        """
        发送消息
        
        Args:
            receiver: 接收者ID
            content: 消息内容
            conversation_type: 会话类型，默认为单聊
            
        Returns:
            失败：包含code和message的字典
            成功：包含code、message_id和message的字典
        """
        if not self.engine:
            return {"code": -1, "message": "引擎实例尚未构建，请先调用initialize初始化SDK"}

        if USER_ID == "":
            return {"code": -1, "message": "未连接"}
            
        try:
            # 根据整数值选择对应的会话类型
            if conversation_type == 1:
                real_conversation_type = RcimConversationType_Private
            elif conversation_type == 2:
                real_conversation_type = RcimConversationType_Group
            else:
                return {"code": -1, "message": "会话类型错误"}
            
            
            # 创建回调数据类
            class SendMessageData:
                def __init__(self):
                    self.result = {"code": -1, "message": ""}
                
                def callback(self, user_data, code, message_id):
                    try:
                        
                        # 处理消息ID（可能是字符串或其他类型）
                        message_id_str = None
                        if isinstance(message_id, str):
                            message_id_str = message_id
                        elif hasattr(message_id, 'data') and message_id.data:
                            # 处理String类型
                            message_id_str = message_id.data.decode('utf-8')
                        elif message_id:
                            # 尝试其他转换方法
                            message_id_str = str(message_id)
                            
                        self.result = {
                            "code": code,
                            "message_id": message_id_str,
                            "message": "发送消息成功" if code == 0 else "发送消息失败"
                        }
                        logger.info(f"发送消息回调: {'成功' if code == 0 else '失败'}, 消息ID: {message_id_str}, 错误码: {code}")
                    except Exception as e:
                        logger.info(f"回调函数内部错误: {e}")
                        self.result = {"code": -1, "message": str(e)}
            
            # 创建回调数据
            callback_data = SendMessageData()
            event = threading.Event()
            # 使用正确的回调函数类型和参数
            def callback_wrapper(user_data, code, message_box):
                # 提取消息ID
                message_id = None
                if message_box and message_box.contents:
                    message_dict = ctypes_to_dict(message_box.contents)
                    message_id = message_dict.get("message_id")
                
                res = callback_data.callback(user_data, code, message_id)
                event.set()
                return res
            
            callback_fn = rcim_client.RcimCodeMessageCb(callback_wrapper)
            
            # 创建一个空的消息回调函数
            def empty_message_callback(user_data, message):
                # 这是一个空的实现，仅用于满足类型要求
                pass
            
            # 定义消息回调类型
            message_callback_fn = rcim_client.RcimMessageCb(empty_message_callback)
            
            message_box_dic = {
                'conv_type':real_conversation_type,
                'target_id':receiver,
                'object_name': 'RC:TxtMsg',
                'content' : {
                    'content':content
                },
                'uid': USER_ID
            }

            # 创建RcimMessageBox结构体实例
            message_box = dict_to_ctypes(RcimMessageBox,message_box_dic)
            # 创建send_message_option对象
            send_option = dict_to_ctypes(RcimSendMessageOption,{})

            # 调用发送函数
            rcim_client.rcim_engine_send_message(
                self.engine[0],  # 使用self.engine[0]获取指针对象 
                message_box,
                send_option,
                None,  # user_data参数设为None
                callback_fn,
                message_callback_fn
            )
            
            # 用事件等待回调完成
            finished = event.wait(timeout=2)
            if not finished:
                logger.info("发送消息超时，未收到回调")
                return {"code": -2, "message": "发送消息超时，未收到回调"}
            # 返回回调的结果
            return callback_data.result
        except Exception as e:
            import traceback
            logger.info(f"发送消息失败: {e}")
            logger.info(f"异常堆栈: {traceback.format_exc()}")
            return {
                "code": -1,
                "message": str(e)
            }
    
    def get_history_messages(self, target_id: str, conversation_type: int = RcimConversationType_Private, count: int = 10, timestamp: int = 0, order: int = 0) -> List[Dict[str, Any]]:
        """
        获取远程历史消息
        
        Args:
            target_id: 目标ID(单聊用户ID或者群ID)
            count: 获取的消息数量，默认为10
            timestamp: 时间戳，默认为0（从最新消息开始）
            order: 排序方式，0为降序，1为升序
            
        Returns:
            失败：包含code和message的字典
            成功：包含code和message数组的字典
        """
        if not self.engine:
            return [{"code": -1, "message": "引擎实例尚未构建，请先调用initialize初始化SDK"}]

        if USER_ID == "":
            return {"code": -1, "message": "未连接"}
        
        if timestamp == 0:
            # 获取当前时间戳(毫秒)
            timestamp = int(time.time() * 1000)
        
        # 创建同步事件
        done_event = threading.Event()

        class GetMessagesData:
            def __init__(self):
                self.messages = []
                self.code = -1

            def callback(self, user_data, code, messages, messages_len):
                logger.info(f"获取远程消息回调: code={code}, message_count={messages_len}")
                self.code = code
                if code == 0 and messages and messages_len > 0:
                    for i in range(messages_len):
                        msg_dict = ctypes_to_dict(messages[i])
                        self.messages.append(msg_dict)
                done_event.set()  # 回调结束，通知主线程
        
        # 创建回调数据
        callback_data = GetMessagesData()
        
        # 使用正确的回调函数类型和参数
        def callback_wrapper(user_data, code, messages, messages_len):
            res = callback_data.callback(user_data, code, messages, messages_len)
            done_event.set()
            return res

        callback_fn = rcim_client.RcimGetMessageListCb(callback_wrapper)
        
        # 转换其他参数为C类型
        count_c = ctypes.c_int(count)
        timestamp_c = ctypes.c_int64(timestamp)
        order_enum = rcim_client.RcimOrder_Descending if order == 0 else rcim_client.RcimOrder_Ascending
        logger.info(f"order: {order_enum}")
        
        # 调用远程历史消息函数
        rcim_client.rcim_engine_get_remote_history_messages(
            self.engine[0],  # 引擎指针
            conversation_type,  # 会话类型（私聊）
            char_pointer_cast(target_id),  # 目标用户ID
            None,  # 频道ID（为空）
            timestamp_c,  # 时间戳
            count_c,  # 消息数量
            order_enum,  # 排序方式
            True,  # 是否包含本地消息
            None,  # user_data
            callback_fn  # 回调函数
        )
        
        # 等待回调，最多5秒
        finished = done_event.wait(timeout=2)

        if not finished:
            logger.info("获取历史消息超时，未收到回调")
            return [{"code": -2, "message": "获取历史消息超时，未收到回调"}]

        if callback_data.code != 0:
            return [{"code": callback_data.code, "message": callback_data.messages}]
        return [{"code": 0, "messages": callback_data.messages}]
        
    def engine_disconnect(self) -> Dict[str, Any]:
        """
        断开与IM服务器的连接
        
        Returns:
            包含code和message的字典
        """
        global USER_ID
        if not self.engine:
            USER_ID = ""
            return {"code": -1, "message": "引擎实例尚未构建，请先调用initialize初始化SDK"}

        if USER_ID == "":
            return {"code": -1, "message": "未连接"}
        
        # 创建回调数据类
        class DisconnectData:
            def __init__(self):
                self.result = {"code": -1, "message": ""}
                
            def callback(self, user_data, code):
                self.result = {
                    "code": code,
                    "message": "断开连接成功" if code == 0 else "断开连接失败"
                }
                if code == 0:
                    global USER_ID
                    USER_ID = ""
                
        # 创建事件用于等待回调完成
        disconnect_event = threading.Event()
        # 创建回调数据
        callback_data = DisconnectData()
        def callback_wrapper(user_data, code):
            res = callback_data.callback(user_data, code)
            disconnect_event.set()
            return res
            
        # 使用正确的回调函数类型
        callback_fn = rcim_client.RcimEngineErrorCb(callback_wrapper)  
        logger.info("断开连接 准备处理") 
        rcim_client.rcim_engine_disconnect(self.engine[0], RcimDisconnectMode_NoPush, None, callback_fn)
        logger.info("断开连接 处理完成") 
        # 等待回调完成,最多等待3秒
        finished = disconnect_event.wait(timeout=2)
        if not finished:
            logger.info("断开连接超时，未收到回调")
            return {"code": -2, "message": "断开连接超时，未收到回调"}
        return callback_data.result
    


    def destroy(self):
        """
        销毁IM SDK
        """
        if self.engine:
            self.engine_disconnect()
        self.engine = None
        self.builder = None

# 创建默认SDK实例，使用默认参数
default_sdk = IMSDK() 