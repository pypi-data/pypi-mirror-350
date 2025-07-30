"""
IM SDK Python封装模块

用于加载和封装Rust Universal IM SDK动态库
"""
# 获取动态库文件的绝对路径
import os
from pathlib import Path
import sys

# 定义lib目录
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
NATIVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIB_DIR = os.path.join(NATIVE_DIR, "lib")

    
from .engine import IMSDK, default_sdk

__all__ = ["IMSDK", "default_sdk"] 
