"""
IM SDK Python Wrapper Module

Used to load and wrap Rust Universal IM SDK dynamic library
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
        Initialize IM SDK and return status
        
        Args:
            app_key: Application's AppKey
            device_id: Device ID
            
        Returns:
            Failure: Dictionary containing code and message
            Success: Dictionary containing code, app_key, device_id and message
        """
        if self.engine:
            return {"code": -1, "message": "Engine instance already built, please call destroy first"}
        # Store application info
        self.app_key = app_key
        self.device_id = device_id
        
        logger.info(f"Initializing IM SDK, AppKey: {app_key}, Device ID: {device_id}, Platform: {PLATFORM}")
        
        try:
            # Prepare initialization parameters
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
            
            # Create parameter struct
            param = dict_to_ctypes(RcimEngineBuilderParam, engine_builder_param)
            
            # Create builder pointer
            builder = ctypes.pointer(ctypes.pointer(RcimEngineBuilder()))
            
            # Call creation function
            ret = rcim_client.rcim_create_engine_builder(param,builder)
            if ret != 0:
                logger.info(f"rcim_create_engine_builder failed, error code: {ret}")
                return {"code": -1, "message": f"rcim_create_engine_builder failed, error code: {ret}"}
            
            # Save builder reference
            self.builder = builder.contents
            
            # Set storage path
            db_path = os.path.join(LIB_DIR, "rust_db")
            # Ensure directory exists
            os.makedirs(db_path, exist_ok=True)
            
            ret = rcim_client.rcim_engine_builder_set_store_path(self.builder, char_pointer_cast(db_path))
            if ret != 0:
                logger.info(f"rcim_engine_builder_set_store_path failed, error code: {ret}")

            # Set navi server
            navi_list = [navi_host]
            char_ptrs = (ctypes.POINTER(ctypes.c_char) * len(navi_list))()
            for i, string in enumerate(navi_list):
                if string is None:
                    char_ptrs[i] = None
                    continue
                # Create c_char array pointer for corresponding string
                char_array = ctypes.create_string_buffer(string.encode('utf-8'))
                char_ptrs[i] = ctypes.cast(char_array, ctypes.POINTER(ctypes.c_char))
            double_ptr = ctypes.cast(char_ptrs, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
            
            ret = rcim_client.rcim_engine_builder_set_navi_server(self.builder, double_ptr,1)
            if ret != 0:
                logger.info(f"rcim_engine_builder_set_navi_server failed, error code: {ret}")

            # Create engine
            engine_ptr = ctypes.pointer(ctypes.pointer(RcimEngineSync()))
            
            logger.info(f"rcim_engine_builder_build about to execute")

            # Build engine
            ret = rcim_client.rcim_engine_builder_build(self.builder, engine_ptr)
            if ret != 0:
                logger.info(f"rcim_engine_builder_build failed, error code: {ret}")
                return {"code": -1, "message": f"rcim_engine_builder_build failed, error code: {ret}"}
            
            # Save engine reference
            self.engine = engine_ptr.contents

            rcim_client.rcim_engine_set_log_filter(self.engine,RcimLogLevel_Debug)

            return {
                "code": 0,
                "app_key": app_key,
                "device_id": device_id,
                "message": "IM SDK initialization successful"
            }
        except Exception as e:
            import traceback
            logger.info(f"IM SDK initialization failed: {e}")
            logger.info(f"Exception stack: {traceback.format_exc()}")
            return {
                "code": -1,
                "message": str(e)
            }

    def engine_connect(self, token: str, timeout_sec: int = 10) -> Dict[str, Any]:
        """
        Connect to Rongcloud service
        
        Args:
            token: User connection token
            timeout_sec: Connection timeout in seconds
            
        Returns:
            Failure: Dictionary containing code and message
            Success: Dictionary containing code, user_id and message
        """
        
        if not self.engine:
            return {"code": -1, "message": "Engine instance not built yet, please call initialize first"}
        
        logger.info(f"Connecting to Rongcloud service, token: {token}..., timeout: {timeout_sec}s")
        
        # Create callback data class
        class ConnectData:
            def __init__(self):
                self.result = {"code": -1, "message": ""}
            
            def callback(self, user_data, code, user_id):

                logger.info(f"rcim_engine_connect callback execution started")
                # Get string from String type
                user_id_str = string_cast(user_id)
                # Assign user_id_str to global variable _USER_ID
                global USER_ID
                USER_ID = user_id_str
                self.result = {
                    "code": code,
                    "user_id": user_id_str if code == 0 else "",
                    "message": "Connection successful" if code == 0 else "Connection failed"  
                }
                logger.info(f"Connection callback: {'successful' if code == 0 else 'failed'}, User ID: {user_id_str}, Error code: {code}")
        
        # Create callback data
        callback_data = ConnectData()
        # Use event to wait for callback completion
        connect_event = threading.Event()
        # Use RcimConnectCb type defined in rcim_client module directly
        # Create callback function
        def callback_wrapper(user_data, code, user_id):
            res = callback_data.callback(user_data, code, user_id)
            connect_event.set()
            return res
        
        # Use correct callback function type
        callback_fn = rcim_client.RcimConnectCb(callback_wrapper)
        
        # Correctly convert token
        token_buffer = char_pointer_cast(token)
        logger.info(f"token_buffer type: {type(token)}")
        logger.info(f"token_buffer type: {type(token_buffer)}")
        
        # Create timeout parameter
        timeout_c = ctypes.c_int(timeout_sec)
        
        logger.info(f"rcim_engine_connect about to execute")
        # Call connect function, note engine instance access method
        rcim_client.rcim_engine_connect(
            self.engine[0],  # Use self.engine[0] to get pointer object
            token_buffer,
            timeout_c,
            None,  # Set user_data parameter to None
            callback_fn
        )
        logger.info(f"rcim_engine_connect execution completed")

        finished = connect_event.wait(timeout=timeout_sec + 1)
        if not finished:
            logger.info("Connection timeout, no callback received")
            return {"code": -2, "message": "Connection timeout, no callback received"}
        # Return callback result
        return callback_data.result
    
    def send_message(self, receiver: str, content: str, conversation_type = RcimConversationType_Private) -> Dict[str, Any]:
        """
        Send message
        
        Args:
            receiver: Recipient ID
            content: Message content
            conversation_type: Conversation type, default is private chat
            
        Returns:
            Failure: Dictionary containing code and message
            Success: Dictionary containing code, message_id and message
        """
        if not self.engine:
            return {"code": -1, "message": "Engine instance not built yet, please call initialize first"}

        if USER_ID == "":
            return {"code": -1, "message": "Not connected"}
            
        try:
            # Choose conversation type based on integer value
            if conversation_type == 1:
                real_conversation_type = RcimConversationType_Private
            elif conversation_type == 2:
                real_conversation_type = RcimConversationType_Group
            else:
                return {"code": -1, "message": "Invalid conversation type"}
            
            
            # Create callback data class
            class SendMessageData:
                def __init__(self):
                    self.result = {"code": -1, "message": ""}
                
                def callback(self, user_data, code, message_id):
                    try:
                        
                        # Handle message ID (could be string or other type)
                        message_id_str = None
                        if isinstance(message_id, str):
                            message_id_str = message_id
                        elif hasattr(message_id, 'data') and message_id.data:
                            # Handle String type
                            message_id_str = message_id.data.decode('utf-8')
                        elif message_id:
                            # Try other conversion methods
                            message_id_str = str(message_id)
                            
                        self.result = {
                            "code": code,
                            "message_id": message_id_str,
                            "message": "Message sent successfully" if code == 0 else "Message sending failed"
                        }
                        logger.info(f"Send message callback: {'successful' if code == 0 else 'failed'}, Message ID: {message_id_str}, Error code: {code}")
                    except Exception as e:
                        logger.info(f"Internal error in callback function: {e}")
                        self.result = {"code": -1, "message": str(e)}
            
            # Create callback data
            callback_data = SendMessageData()
            event = threading.Event()
            # Use correct callback function type and parameters
            def callback_wrapper(user_data, code, message_box):
                # Extract message ID
                message_id = None
                if message_box and message_box.contents:
                    message_dict = ctypes_to_dict(message_box.contents)
                    message_id = message_dict.get("message_id")
                
                res = callback_data.callback(user_data, code, message_id)
                event.set()
                return res
            
            callback_fn = rcim_client.RcimCodeMessageCb(callback_wrapper)
            
            # Create an empty message callback function
            def empty_message_callback(user_data, message):
                # This is an empty implementation, just to satisfy type requirements
                pass
            
            # Define message callback type
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

            # Create RcimMessageBox struct instance
            message_box = dict_to_ctypes(RcimMessageBox,message_box_dic)
            # Create send_message_option object
            send_option = dict_to_ctypes(RcimSendMessageOption,{})

            # Call send function
            rcim_client.rcim_engine_send_message(
                self.engine[0],  # Use self.engine[0] to get pointer object 
                message_box,
                send_option,
                None,  # Set user_data parameter to None
                callback_fn,
                message_callback_fn
            )
            
            # Use event to wait for callback completion
            finished = event.wait(timeout=2)
            if not finished:
                logger.info("Message sending timeout, no callback received")
                return {"code": -2, "message": "Message sending timeout, no callback received"}
            # Return callback result
            return callback_data.result
        except Exception as e:
            import traceback
            logger.info(f"Message sending failed: {e}")
            logger.info(f"Exception stack: {traceback.format_exc()}")
            return {
                "code": -1,
                "message": str(e)
            }
    
    def get_history_messages(self, target_id: str, conversation_type: int = RcimConversationType_Private, count: int = 10, timestamp: int = 0, order: int = 0) -> List[Dict[str, Any]]:
        """
        Get remote historical messages
        
        Args:
            target_id: Target ID (private user ID or group ID)
            conversation_type: Conversation type, default is private chat
            count: Number of messages to retrieve, default is 10
            timestamp: Timestamp, default is 0 (start from latest message)
            order: Sort order, 0 for descending, 1 for ascending
            
        Returns:
            Failure: Dictionary containing code and message
            Success: Dictionary containing code and message array
        """
        if not self.engine:
            return [{"code": -1, "message": "Engine instance not built yet, please call initialize first"}]

        if USER_ID == "":
            return {"code": -1, "message": "Not connected"}
        
        if timestamp == 0:
            # Get current timestamp (milliseconds)
            timestamp = int(time.time() * 1000)
        
        # Create synchronization event
        done_event = threading.Event()

        class GetMessagesData:
            def __init__(self):
                self.messages = []
                self.code = -1

            def callback(self, user_data, code, messages, messages_len):
                logger.info(f"Get remote messages callback: code={code}, message_count={messages_len}")
                self.code = code
                if code == 0 and messages and messages_len > 0:
                    for i in range(messages_len):
                        msg_dict = ctypes_to_dict(messages[i])
                        self.messages.append(msg_dict)
                done_event.set()  # Callback ended, notify main thread
        
        # Create callback data
        callback_data = GetMessagesData()
        
        # Use correct callback function type and parameters
        def callback_wrapper(user_data, code, messages, messages_len):
            res = callback_data.callback(user_data, code, messages, messages_len)
            done_event.set()
            return res

        callback_fn = rcim_client.RcimGetMessageListCb(callback_wrapper)
        
        # Convert other parameters to C types
        count_c = ctypes.c_int(count)
        timestamp_c = ctypes.c_int64(timestamp)
        order_enum = rcim_client.RcimOrder_Descending if order == 0 else rcim_client.RcimOrder_Ascending
        logger.info(f"order: {order_enum}")
        
        # Call remote historical messages function
        rcim_client.rcim_engine_get_remote_history_messages(
            self.engine[0],  # Engine pointer
            conversation_type,  # Conversation type (private)
            char_pointer_cast(target_id),  # Target user ID
            None,  # Channel ID (empty)
            timestamp_c,  # Timestamp
            count_c,  # Message count
            order_enum,  # Sort order
            True,  # Include local messages
            None,  # user_data
            callback_fn  # Callback function
        )
        
        # Wait for callback, maximum 5 seconds
        finished = done_event.wait(timeout=2)

        if not finished:
            logger.info("Get historical messages timeout, no callback received")
            return [{"code": -2, "message": "Get historical messages timeout, no callback received"}]

        if callback_data.code != 0:
            return [{"code": callback_data.code, "message": callback_data.messages}]
        return [{"code": 0, "messages": callback_data.messages}]
        
    def engine_disconnect(self) -> Dict[str, Any]:
        """
        Disconnect from IM server
        
        Returns:
            Dictionary containing code and message
        """
        global USER_ID
        if not self.engine:
            USER_ID = ""
            return {"code": -1, "message": "Engine instance not built yet, please call initialize first"}

        if USER_ID == "":
            return {"code": -1, "message": "Not connected"}
        
        # Create callback data class
        class DisconnectData:
            def __init__(self):
                self.result = {"code": -1, "message": ""}
                
            def callback(self, user_data, code):
                self.result = {
                    "code": code,
                    "message": "Disconnection successful" if code == 0 else "Disconnection failed"
                }
                if code == 0:
                    global USER_ID
                    USER_ID = ""
                
        # Create event for waiting callback completion
        disconnect_event = threading.Event()
        # Create callback data
        callback_data = DisconnectData()
        def callback_wrapper(user_data, code):
            res = callback_data.callback(user_data, code)
            disconnect_event.set()
            return res
            
        # Use correct callback function type
        callback_fn = rcim_client.RcimEngineErrorCb(callback_wrapper)  
        logger.info("Disconnection preparation") 
        rcim_client.rcim_engine_disconnect(self.engine[0], RcimDisconnectMode_NoPush, None, callback_fn)
        logger.info("Disconnection completed") 
        # Wait for callback completion, maximum 3 seconds
        finished = disconnect_event.wait(timeout=2)
        if not finished:
            logger.info("Disconnection timeout, no callback received")
            return {"code": -2, "message": "Disconnection timeout, no callback received"}
        return callback_data.result
    


    def destroy(self):
        """
        Destroy IM SDK
        """
        if self.engine:
            self.engine_disconnect()
        self.engine = None
        self.builder = None

# Create default SDK instance using default parameters
default_sdk = IMSDK() 