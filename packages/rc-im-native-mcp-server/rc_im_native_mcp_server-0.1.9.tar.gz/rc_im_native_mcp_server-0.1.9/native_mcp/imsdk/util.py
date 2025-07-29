import ctypes
import json
import random
import string
from _ctypes import _Pointer


def dict_to_ctypes(auto_struct, data):
    """
    自动化从字典到 ctypes 结构体的转换。

    参数:
    - auto_struct: ctypes.Structure 的子类，即目标结构体类型。
    - data: 字典，包含与结构体字段对应的键值对。

    返回:
    - auto_struct 实例，其字段已根据 data 中的数据初始化。
    """
    # 创建结构体实例
    struct_instance = auto_struct()
    field_names = []
    if not hasattr(struct_instance, '_fields_') or not data:
        return data or struct_instance

    # 遍历结构体的所有字段
    for field_name, field_type in struct_instance._fields_:
        field_names.append(field_name)
        if field_name in data:
            value = data[field_name]
            if value is None:
                continue
            # 根据字段类型进行适当的处理
            if issubclass(field_type, ctypes.POINTER(ctypes.c_char)):
                if isinstance(value, str):
                    value = value.encode('utf-8')
                elif isinstance(value, dict):
                    value = json.dumps(value).encode('utf-8')
                else:
                    value = str(value).encode('utf-8')
                buffer = ctypes.create_string_buffer(value)
                setattr(struct_instance, field_name, buffer)
            elif issubclass(field_type, (
                    ctypes.c_int64, ctypes.c_uint64, ctypes.c_uint, ctypes.c_int, ctypes.c_long,
                    ctypes.c_longlong,
                    ctypes.c_ulong)):
                setattr(struct_instance, field_name, int(value))
            elif issubclass(field_type, _Pointer):
                if isinstance(value, list):
                    _data = None
                    if field_type == ctypes.POINTER(ctypes.POINTER(ctypes.c_char)):
                        char_ptrs = (ctypes.POINTER(ctypes.c_char) * len(value))()
                        for i, _string in enumerate(value):
                            # 创建对应字符串的 c_char 数组，并获取其指针
                            char_array = ctypes.create_string_buffer(_string.encode('utf-8'))
                            char_ptrs[i] = ctypes.cast(char_array, ctypes.POINTER(ctypes.c_char))
                        _data = ctypes.cast(char_ptrs, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
                    elif field_type == ctypes.c_int:
                        _data = (ctypes.POINTER(ctypes.c_uint) * len(value))()
                        for i, arg in enumerate(value):
                            _data[i] = ctypes.pointer(ctypes.c_uint(arg))
                    else:
                        _data = (field_type._type_ * len(value))()
                        for i, arg in enumerate(value):
                            _data[i] = dict_to_ctypes(field_type._type_, arg)
                    setattr(struct_instance, field_name, _data)
                else:
                    setattr(struct_instance, field_name,
                            ctypes.pointer(dict_to_ctypes(field_type._type_, value)))
            elif issubclass(field_type, ctypes.Structure):
                setattr(struct_instance, field_name, dict_to_ctypes(field_type, value))
            else:
                setattr(struct_instance, field_name, value)
    for i in data.keys():
        if i not in field_names:
            raise Exception(f"字段 {i} 不在结构体中")

    return struct_instance


def decode_read_receipt_info(auto_struct):
    try:
        respond_user_vec_len = auto_struct.read_receipt_info.contents.respond_user_vec_len
        respond_user_vec = []
        for i in range(respond_user_vec_len):
            respond_user_vec.append(ctypes_to_dict(auto_struct.read_receipt_info.contents.respond_user_vec[i]))
        return {
            'is_read_receipt_message': auto_struct.read_receipt_info.contents.is_read_receipt_message,
            'has_respond': auto_struct.read_receipt_info.contents.has_respond,
            'respond_user_vec': respond_user_vec,
            'respond_user_vec_len': respond_user_vec_len
        }
    except (ValueError, AttributeError) as e:
        if 'NULL' in str(e):
            return None

def decode_read_receipt_info_v2(auto_struct):
    try:
        respond_user_vec_len = auto_struct.read_receipt_info_v2.contents.respond_user_vec_len
        respond_user_vec = []
        for i in range(respond_user_vec_len):
            respond_user_vec.append(ctypes_to_dict(auto_struct.read_receipt_info_v2.contents.respond_user_vec[i]))
        return {
            'read_count': auto_struct.read_receipt_info_v2.contents.read_count,
            'total_count': auto_struct.read_receipt_info_v2.contents.total_count,
            'has_respond': auto_struct.read_receipt_info_v2.contents.has_respond,
            'respond_user_vec': respond_user_vec,
            'respond_user_vec_len': respond_user_vec_len
        }
    except (ValueError, AttributeError) as e:
        if 'NULL' in str(e):
            return None


def ctypes_to_dict(auto_struct):
    """
    :param auto_struct: ctypes.Structure 的子类，即目标结构体类型。
    :return:
    """
    # 创建空字典
    data = {}
    if auto_struct is None:
        return data
    # 遍历结构体的所有字段
    if isinstance(auto_struct, ctypes.Structure):
        if not hasattr(auto_struct, '_fields_'):
            return auto_struct
        for field_name, field_type in auto_struct._fields_:
            if 'PADDING' in field_name:
                continue
            if field_name == 'read_receipt_info':
                data[field_name] = decode_read_receipt_info(auto_struct)
                continue
            if field_name == 'read_receipt_info_v2':
                data[field_name] = decode_read_receipt_info_v2(auto_struct)
                continue
            data[field_name] = ctypes_to_dict(getattr(auto_struct, field_name))
        return data
    elif isinstance(auto_struct, _Pointer):
        try:
            if isinstance(auto_struct.contents, ctypes.c_char):
                c_char_p_string = ctypes.cast(auto_struct, ctypes.c_char_p)
                python_string = c_char_p_string.value.decode('utf-8')
                return python_string
            elif isinstance(auto_struct.contents,
                            (ctypes.c_int64, ctypes.c_uint64, ctypes.c_uint, ctypes.c_int,
                             ctypes.c_long,
                             ctypes.c_longlong,
                             ctypes.c_ulong)):
                return int(auto_struct.contents.value)
            elif isinstance(auto_struct.contents, ctypes.c_bool):
                return bool(auto_struct.contents.value)
            elif isinstance(auto_struct.contents, (ctypes.Structure, _Pointer)):
                return ctypes_to_dict(auto_struct.contents)
        except (ValueError, AttributeError) as e:
            if 'NULL' in str(e):
                return None
            return auto_struct
    else:
        return auto_struct
    return data


class RCUtil:
    @staticmethod
    def random_str(length):
        characters = string.ascii_letters + string.digits

        # 从字符集中随机选择8个字符
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

class MessageTool:

    def __init__(self, message_ret):
        if not isinstance(message_ret, dict):
            raise ValueError("message_ret 类型必须为 dict")
        self.message_box = message_ret
        if message_ret.get("message"):
            self.message_box: dict = message_ret.get("message")

    def get_conversation_type(self):
        return self.message_box.get("conversation_type")

    def get_target_id(self):
        return self.message_box.get('target_id')

    def get_channel_id(self):
        return self.message_box.get("channel_id")

    def get_message_id(self):
        return self.message_box.get("message_id")

    def get_direction(self):
        return self.message_box.get("direction")

    def get_received_status(self):
        return self.message_box.get("received_status")

    def get_sent_status(self):
        return self.message_box.get("sent_status")

    def get_received_time(self):
        return self.message_box.get("received_time")

    def get_sent_time(self):
        return self.message_box.get("sent_time")

    def get_object_name(self):
        return self.message_box.get("object_name")

    def get_content(self):
        return self.message_box.get("content")

    def get_uid(self):
        return self.message_box.get("uid")

    def get_extra(self):
        return self.message_box.get("extra")

    def get_disable_notification(self):
        return self.message_box.get("disable_notification")

    def get_push_config(self):
        return self.message_box.get("push_config")

    def get_is_offline(self):
        return self.message_box.get("is_offline")

    def get_ext_support(self):
        return self.message_box.get("ext_support")

    def get_ext_content(self):
        return self.message_box.get("ext_content")


def get_class_vars(cls):
    _data = {}
    for attr, value in vars(cls).items():
        if not attr.startswith('__'):  # 过滤掉 Python 的内置属性
            _data[attr] = value
    return _data
