"""
IM SDK 辅助工具模块

提供与 rcim_client 模块一起使用的辅助函数
"""

import ctypes
from typing import Dict, Any

def string_cast(value):
    """将ctypes字符指针转换为Python字符串"""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='replace')
    if isinstance(value, str):
        return value
    try:
        return ctypes.cast(value, ctypes.c_char_p).value.decode('utf-8', errors='replace')
    except:
        return str(value)

def char_pointer_cast(value):
    """将Python字符串转换为ctypes字符指针"""
    if value is None:
        return None
    if isinstance(value, bytes):
        return ctypes.c_char_p(value)
    if isinstance(value, str):
        return ctypes.c_char_p(value.encode('utf-8'))
    return value

def ctypes_to_dict(obj):
    """将ctypes结构体转换为Python字典"""
    if obj is None:
        return {}
    result = {}
    for field_name, _ in getattr(obj, "_fields_", []):
        value = getattr(obj, field_name, None)
        if isinstance(value, (bytes, ctypes.c_char_p)):
            result[field_name] = string_cast(value)
        elif hasattr(value, "_fields_"):
            result[field_name] = ctypes_to_dict(value)
        else:
            result[field_name] = value
    return result 