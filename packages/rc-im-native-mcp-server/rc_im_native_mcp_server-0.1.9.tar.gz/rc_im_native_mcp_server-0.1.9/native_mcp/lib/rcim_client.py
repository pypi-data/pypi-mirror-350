# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-isysroot', '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 8
#
import ctypes
import sys
import os


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                type_ = type_._type_
                if hasattr(type_, 'as_dict'):
                    value = [type_.as_dict(v) for v in value]
                else:
                    value = [i for i in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass



def string_cast(char_pointer, encoding='utf-8', errors='strict'):
    value = ctypes.cast(char_pointer, ctypes.c_char_p).value
    if value is not None and encoding is not None:
        value = value.decode(encoding, errors=errors)
    return value


def char_pointer_cast(string, encoding='utf-8'):
    if encoding is not None:
        try:
            string = string.encode(encoding)
        except AttributeError:
            # In Python3, bytes has no encode attribute
            pass
    string = ctypes.c_char_p(string)
    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))



c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 8:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*8

class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

# libraries['FIXME_STUB'] explanation
# As you did not list (-l libraryname.so) a library that exports this function
# This is a non-working stub instead. 
# You can either re-run clan2py with -l /path/to/library.so
# Or manually fix this by comment the ctypes.CDLL loading
_libraries = {}

# 根据平台加载不同后缀的动态库
if sys.platform == 'darwin':
    _libraries['FIXME_STUB'] = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'librust_universal_imsdk.dylib'))
elif sys.platform == 'win32':
    _libraries['FIXME_STUB'] = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'rust_universal_imsdk.dll'))
elif sys.platform == 'linux':
    _libraries['FIXME_STUB'] = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'librust_universal_imsdk.so'))
else:
    raise RuntimeError(f'不支持的操作系统平台: {sys.platform}')



# values for enumeration 'RcimAppState'
RcimAppState__enumvalues = {
    0: 'RcimAppState_Foreground',
    1: 'RcimAppState_Background',
    2: 'RcimAppState_Hangup',
    3: 'RcimAppState_Terminate',
}
RcimAppState_Foreground = 0
RcimAppState_Background = 1
RcimAppState_Hangup = 2
RcimAppState_Terminate = 3
RcimAppState = ctypes.c_uint32 # enum

# values for enumeration 'RcimAreaCode'
RcimAreaCode__enumvalues = {
    1: 'RcimAreaCode_Bj',
    2: 'RcimAreaCode_Sg',
    3: 'RcimAreaCode_Na',
    4: 'RcimAreaCode_SgB',
    5: 'RcimAreaCode_Sa',
}
RcimAreaCode_Bj = 1
RcimAreaCode_Sg = 2
RcimAreaCode_Na = 3
RcimAreaCode_SgB = 4
RcimAreaCode_Sa = 5
RcimAreaCode = ctypes.c_uint32 # enum

# values for enumeration 'RcimChatroomMemberActionType'
RcimChatroomMemberActionType__enumvalues = {
    0: 'RcimChatroomMemberActionType_Quit',
    1: 'RcimChatroomMemberActionType_Join',
}
RcimChatroomMemberActionType_Quit = 0
RcimChatroomMemberActionType_Join = 1
RcimChatroomMemberActionType = ctypes.c_uint32 # enum

# values for enumeration 'RcimChatroomMemberBannedEventType'
RcimChatroomMemberBannedEventType__enumvalues = {
    0: 'RcimChatroomMemberBannedEventType_UnmuteUser',
    1: 'RcimChatroomMemberBannedEventType_MuteUsers',
    2: 'RcimChatroomMemberBannedEventType_UnmuteAll',
    3: 'RcimChatroomMemberBannedEventType_MuteAll',
    4: 'RcimChatroomMemberBannedEventType_RemoveWhitelist',
    5: 'RcimChatroomMemberBannedEventType_AddWhitelist',
    6: 'RcimChatroomMemberBannedEventType_UnmuteGlobal',
    7: 'RcimChatroomMemberBannedEventType_MuteGlobal',
}
RcimChatroomMemberBannedEventType_UnmuteUser = 0
RcimChatroomMemberBannedEventType_MuteUsers = 1
RcimChatroomMemberBannedEventType_UnmuteAll = 2
RcimChatroomMemberBannedEventType_MuteAll = 3
RcimChatroomMemberBannedEventType_RemoveWhitelist = 4
RcimChatroomMemberBannedEventType_AddWhitelist = 5
RcimChatroomMemberBannedEventType_UnmuteGlobal = 6
RcimChatroomMemberBannedEventType_MuteGlobal = 7
RcimChatroomMemberBannedEventType = ctypes.c_uint32 # enum

# values for enumeration 'RcimChatroomMemberBlockedEventType'
RcimChatroomMemberBlockedEventType__enumvalues = {
    0: 'RcimChatroomMemberBlockedEventType_Unblock',
    1: 'RcimChatroomMemberBlockedEventType_Block',
}
RcimChatroomMemberBlockedEventType_Unblock = 0
RcimChatroomMemberBlockedEventType_Block = 1
RcimChatroomMemberBlockedEventType = ctypes.c_uint32 # enum

# values for enumeration 'RcimChatroomMultiClientSyncEventType'
RcimChatroomMultiClientSyncEventType__enumvalues = {
    0: 'RcimChatroomMultiClientSyncEventType_Quit',
    1: 'RcimChatroomMultiClientSyncEventType_Join',
}
RcimChatroomMultiClientSyncEventType_Quit = 0
RcimChatroomMultiClientSyncEventType_Join = 1
RcimChatroomMultiClientSyncEventType = ctypes.c_uint32 # enum

# values for enumeration 'RcimChatroomMultiClientSyncQuitType'
RcimChatroomMultiClientSyncQuitType__enumvalues = {
    1: 'RcimChatroomMultiClientSyncQuitType_Manual',
    2: 'RcimChatroomMultiClientSyncQuitType_Kick',
}
RcimChatroomMultiClientSyncQuitType_Manual = 1
RcimChatroomMultiClientSyncQuitType_Kick = 2
RcimChatroomMultiClientSyncQuitType = ctypes.c_uint32 # enum

# values for enumeration 'RcimChatroomStatus'
RcimChatroomStatus__enumvalues = {
    0: 'RcimChatroomStatus_Idle',
    1: 'RcimChatroomStatus_Joining',
    2: 'RcimChatroomStatus_Joined',
    3: 'RcimChatroomStatus_JoinFailed',
    4: 'RcimChatroomStatus_Leaving',
    5: 'RcimChatroomStatus_Left',
    6: 'RcimChatroomStatus_LeaveFailed',
    7: 'RcimChatroomStatus_DestroyManually',
    8: 'RcimChatroomStatus_DestroyAuto',
}
RcimChatroomStatus_Idle = 0
RcimChatroomStatus_Joining = 1
RcimChatroomStatus_Joined = 2
RcimChatroomStatus_JoinFailed = 3
RcimChatroomStatus_Leaving = 4
RcimChatroomStatus_Left = 5
RcimChatroomStatus_LeaveFailed = 6
RcimChatroomStatus_DestroyManually = 7
RcimChatroomStatus_DestroyAuto = 8
RcimChatroomStatus = ctypes.c_uint32 # enum

# values for enumeration 'RcimCloudType'
RcimCloudType__enumvalues = {
    0: 'RcimCloudType_PublicCloud',
    1: 'RcimCloudType_PrivateCloud',
    2: 'RcimCloudType_PrivateCloud104',
}
RcimCloudType_PublicCloud = 0
RcimCloudType_PrivateCloud = 1
RcimCloudType_PrivateCloud104 = 2
RcimCloudType = ctypes.c_uint32 # enum

# values for enumeration 'RcimConnectionStatus'
RcimConnectionStatus__enumvalues = {
    0: 'RcimConnectionStatus_Idle',
    1: 'RcimConnectionStatus_Connecting',
    2: 'RcimConnectionStatus_Connected',
    3: 'RcimConnectionStatus_Disconnecting',
    10: 'RcimConnectionStatus_DisconnectNetworkUnavailable',
    11: 'RcimConnectionStatus_DisconnectUserLogout',
    12: 'RcimConnectionStatus_DisconnectLicenseExpired',
    13: 'RcimConnectionStatus_DisconnectLicenseMismatch',
    14: 'RcimConnectionStatus_DisconnectIllegalProtocolVersion',
    15: 'RcimConnectionStatus_DisconnectIdReject',
    16: 'RcimConnectionStatus_DisconnectPlatformUnavailable',
    17: 'RcimConnectionStatus_DisconnectTokenIncorrect',
    18: 'RcimConnectionStatus_DisconnectNotAuthorized',
    19: 'RcimConnectionStatus_DisconnectPackageNameInvalid',
    20: 'RcimConnectionStatus_DisconnectAppBlockOrDelete',
    21: 'RcimConnectionStatus_DisconnectUserBlocked',
    22: 'RcimConnectionStatus_DisconnectUserKicked',
    23: 'RcimConnectionStatus_DisconnectTokenExpired',
    24: 'RcimConnectionStatus_DisconnectDeviceError',
    25: 'RcimConnectionStatus_DisconnectHostnameError',
    26: 'RcimConnectionStatus_DisconnectOtherDeviceLogin',
    27: 'RcimConnectionStatus_DisconnectConcurrentLimitError',
    28: 'RcimConnectionStatus_DisconnectClusterError',
    29: 'RcimConnectionStatus_DisconnectAppAuthFailed',
    30: 'RcimConnectionStatus_DisconnectOneTimePasswordUsed',
    31: 'RcimConnectionStatus_DisconnectPlatformError',
    32: 'RcimConnectionStatus_DisconnectUserDeleteAccount',
    33: 'RcimConnectionStatus_DisconnectConnectionTimeout',
    34: 'RcimConnectionStatus_DisconnectDatabaseOpenFailed',
}
RcimConnectionStatus_Idle = 0
RcimConnectionStatus_Connecting = 1
RcimConnectionStatus_Connected = 2
RcimConnectionStatus_Disconnecting = 3
RcimConnectionStatus_DisconnectNetworkUnavailable = 10
RcimConnectionStatus_DisconnectUserLogout = 11
RcimConnectionStatus_DisconnectLicenseExpired = 12
RcimConnectionStatus_DisconnectLicenseMismatch = 13
RcimConnectionStatus_DisconnectIllegalProtocolVersion = 14
RcimConnectionStatus_DisconnectIdReject = 15
RcimConnectionStatus_DisconnectPlatformUnavailable = 16
RcimConnectionStatus_DisconnectTokenIncorrect = 17
RcimConnectionStatus_DisconnectNotAuthorized = 18
RcimConnectionStatus_DisconnectPackageNameInvalid = 19
RcimConnectionStatus_DisconnectAppBlockOrDelete = 20
RcimConnectionStatus_DisconnectUserBlocked = 21
RcimConnectionStatus_DisconnectUserKicked = 22
RcimConnectionStatus_DisconnectTokenExpired = 23
RcimConnectionStatus_DisconnectDeviceError = 24
RcimConnectionStatus_DisconnectHostnameError = 25
RcimConnectionStatus_DisconnectOtherDeviceLogin = 26
RcimConnectionStatus_DisconnectConcurrentLimitError = 27
RcimConnectionStatus_DisconnectClusterError = 28
RcimConnectionStatus_DisconnectAppAuthFailed = 29
RcimConnectionStatus_DisconnectOneTimePasswordUsed = 30
RcimConnectionStatus_DisconnectPlatformError = 31
RcimConnectionStatus_DisconnectUserDeleteAccount = 32
RcimConnectionStatus_DisconnectConnectionTimeout = 33
RcimConnectionStatus_DisconnectDatabaseOpenFailed = 34
RcimConnectionStatus = ctypes.c_uint32 # enum

# values for enumeration 'RcimConversationType'
RcimConversationType__enumvalues = {
    0: 'RcimConversationType_NotSupportedYet',
    1: 'RcimConversationType_Private',
    2: 'RcimConversationType_Discussion',
    3: 'RcimConversationType_Group',
    4: 'RcimConversationType_Chatroom',
    5: 'RcimConversationType_CustomerService',
    6: 'RcimConversationType_System',
    7: 'RcimConversationType_AppPublicService',
    8: 'RcimConversationType_PublicService',
    9: 'RcimConversationType_PushService',
    10: 'RcimConversationType_UltraGroup',
    11: 'RcimConversationType_Encrypted',
    12: 'RcimConversationType_RtcRoom',
}
RcimConversationType_NotSupportedYet = 0
RcimConversationType_Private = 1
RcimConversationType_Discussion = 2
RcimConversationType_Group = 3
RcimConversationType_Chatroom = 4
RcimConversationType_CustomerService = 5
RcimConversationType_System = 6
RcimConversationType_AppPublicService = 7
RcimConversationType_PublicService = 8
RcimConversationType_PushService = 9
RcimConversationType_UltraGroup = 10
RcimConversationType_Encrypted = 11
RcimConversationType_RtcRoom = 12
RcimConversationType = ctypes.c_uint32 # enum

# values for enumeration 'RcimDatabaseStatus'
RcimDatabaseStatus__enumvalues = {
    0: 'RcimDatabaseStatus_Idle',
    1: 'RcimDatabaseStatus_OpenSuccess',
    2: 'RcimDatabaseStatus_OpenFailed',
    3: 'RcimDatabaseStatus_Upgrading',
    4: 'RcimDatabaseStatus_UpgradeSuccess',
    5: 'RcimDatabaseStatus_UpgradeFailed',
    127: 'RcimDatabaseStatus_Error',
}
RcimDatabaseStatus_Idle = 0
RcimDatabaseStatus_OpenSuccess = 1
RcimDatabaseStatus_OpenFailed = 2
RcimDatabaseStatus_Upgrading = 3
RcimDatabaseStatus_UpgradeSuccess = 4
RcimDatabaseStatus_UpgradeFailed = 5
RcimDatabaseStatus_Error = 127
RcimDatabaseStatus = ctypes.c_uint32 # enum

# values for enumeration 'RcimDevLogLevel'
RcimDevLogLevel__enumvalues = {
    1: 'RcimDevLogLevel_Error',
    2: 'RcimDevLogLevel_Warn',
    3: 'RcimDevLogLevel_Info',
    4: 'RcimDevLogLevel_Debug',
    5: 'RcimDevLogLevel_Trace',
}
RcimDevLogLevel_Error = 1
RcimDevLogLevel_Warn = 2
RcimDevLogLevel_Info = 3
RcimDevLogLevel_Debug = 4
RcimDevLogLevel_Trace = 5
RcimDevLogLevel = ctypes.c_uint32 # enum

# values for enumeration 'RcimDisconnectMode'
RcimDisconnectMode__enumvalues = {
    2: 'RcimDisconnectMode_KeepPush',
    4: 'RcimDisconnectMode_NoPush',
}
RcimDisconnectMode_KeepPush = 2
RcimDisconnectMode_NoPush = 4
RcimDisconnectMode = ctypes.c_uint32 # enum

# values for enumeration 'RcimEngineError'
RcimEngineError__enumvalues = {
    0: 'RcimEngineError_Success',
    405: 'RcimEngineError_RejectedByBlackList',
    407: 'RcimEngineError_NotWhitelisted',
    20106: 'RcimEngineError_ForbiddenInPrivateChat',
    20109: 'RcimEngineError_ConversationNotSupportMessage',
    20604: 'RcimEngineError_MessageSendOverFrequency',
    20607: 'RcimEngineError_RequestOverFrequency',
    21501: 'RcimEngineError_MessageIncludeSensitiveWord',
    21502: 'RcimEngineError_MessageReplacedSensitiveWord',
    22406: 'RcimEngineError_NotInGroup',
    22408: 'RcimEngineError_ForbiddenInGroupChat',
    23408: 'RcimEngineError_ForbiddenInChatroom',
    23409: 'RcimEngineError_ChatroomKicked',
    23410: 'RcimEngineError_ChatroomNotExist',
    23411: 'RcimEngineError_ChatroomIsFull',
    23406: 'RcimEngineError_NotInChatroom',
    23407: 'RcimEngineError_GetUserError',
    23412: 'RcimEngineError_ChatroomInvalidParameter',
    23413: 'RcimEngineError_QueryChatroomHistoryError',
    23414: 'RcimEngineError_RoamingServiceUnavailableChatroom',
    23423: 'RcimEngineError_ChatroomKvCountExceed',
    23424: 'RcimEngineError_ChatroomKvOverwriteInvalidKey',
    23425: 'RcimEngineError_ChatroomKvCallAPIExceed',
    23426: 'RcimEngineError_ChatroomKvStoreUnavailable',
    23427: 'RcimEngineError_ChatroomKvNotExist',
    23428: 'RcimEngineError_ChatroomKvNotAllSuccess',
    23429: 'RcimEngineError_ChatroomKvLimit',
    23431: 'RcimEngineError_ChatroomKvConcurrentError',
    25101: 'RcimEngineError_RecallParameterInvalid',
    25102: 'RcimEngineError_MessageStorageServiceUnavailable',
    25107: 'RcimEngineError_RecallMessageUserInvalid',
    26001: 'RcimEngineError_PushSettingParameterInvalid',
    26002: 'RcimEngineError_SettingSyncFailed',
    26009: 'RcimEngineError_InvalidArgumentMessageUid',
    26107: 'RcimEngineError_RequestUploadTokenSizeError',
    29201: 'RcimEngineError_InvalidPublicService',
    30001: 'RcimEngineError_ConnectionClosed',
    30027: 'RcimEngineError_ConnectionClosing',
    30003: 'RcimEngineError_SocketRecvTimeout',
    30004: 'RcimEngineError_NaviReqFailed',
    30005: 'RcimEngineError_NaviReqTimeout',
    30016: 'RcimEngineError_MsgSizeOutOfLimit',
    30022: 'RcimEngineError_SocketSendTimeout',
    30024: 'RcimEngineError_NaviRespTokenIncorrect',
    30026: 'RcimEngineError_NaviLicenseMismatch',
    34026: 'RcimEngineError_HttpReqFailed',
    34027: 'RcimEngineError_HttpReqTimeout',
    31001: 'RcimEngineError_ConnectIllegalProtocolVersion',
    31002: 'RcimEngineError_ConnectIdReject',
    31003: 'RcimEngineError_ConnectPlatformUnavailable',
    31004: 'RcimEngineError_ConnectTokenIncorrect',
    31005: 'RcimEngineError_ConnectNotAuthorized',
    31006: 'RcimEngineError_ConnectRedirect',
    31007: 'RcimEngineError_ConnectPackageNameInvalid',
    31008: 'RcimEngineError_ConnectAppBlockOrDelete',
    31009: 'RcimEngineError_ConnectUserBlocked',
    31010: 'RcimEngineError_DisconnectUserKicked',
    31011: 'RcimEngineError_DisconnectUserBlocked',
    31012: 'RcimEngineError_DisconnectUserLogout',
    31014: 'RcimEngineError_SocketConnectionFailed',
    31015: 'RcimEngineError_SocketShutdownFailed',
    31016: 'RcimEngineError_ConnectionCancel',
    31020: 'RcimEngineError_ConnectTokenExpired',
    31021: 'RcimEngineError_ConnectDeviceError',
    31022: 'RcimEngineError_ConnectHostnameError',
    31023: 'RcimEngineError_ConnectOtherDeviceLogin',
    31024: 'RcimEngineError_ConnectConcurrentLimitError',
    31025: 'RcimEngineError_ConnectClusterError',
    31026: 'RcimEngineError_ConnectAppAuthFailed',
    31027: 'RcimEngineError_ConnectOneTimePasswordUsed',
    31028: 'RcimEngineError_ConnectPlatformError',
    31029: 'RcimEngineError_ConnectUserDeleteAccount',
    31030: 'RcimEngineError_ConnectLicenseExpired',
    31510: 'RcimEngineError_KvStoreNotOpened',
    31511: 'RcimEngineError_KvStoreOpenFailed',
    31512: 'RcimEngineError_KvStoreIOError',
    31513: 'RcimEngineError_KvStoreSerializationError',
    31610: 'RcimEngineError_JsonParserFailed',
    31611: 'RcimEngineError_ImageFormatError',
    31612: 'RcimEngineError_RequestUploadTokenError',
    31613: 'RcimEngineError_GetUploadTokenError',
    31614: 'RcimEngineError_SightMessageCompressError',
    33200: 'RcimEngineError_RequestCanceled',
    33202: 'RcimEngineError_DownloadRequestExist',
    33204: 'RcimEngineError_RequestPaused',
    33205: 'RcimEngineError_DownloadTaskNotExist',
    33206: 'RcimEngineError_UploadTaskNotExist',
    33207: 'RcimEngineError_MediaMessageHandlerError',
    32061: 'RcimEngineError_ConnectRefused',
    33000: 'RcimEngineError_MessageSavedError',
    33006: 'RcimEngineError_ConnectionInProcess',
    33007: 'RcimEngineError_CloudStorageForHistoryMessageDisable',
    34001: 'RcimEngineError_ConnectionExists',
    34003: 'RcimEngineError_GifMessageSizeOutOfLimit',
    34006: 'RcimEngineError_ConnectionTimeout',
    34008: 'RcimEngineError_MessageCantExpand',
    34010: 'RcimEngineError_MessageExpansionSizeLimitExceed',
    34011: 'RcimEngineError_UploadMediaFailed',
    34014: 'RcimEngineError_GroupReadReceiptVersionNotSupport',
    34016: 'RcimEngineError_UserSettingUnavailable',
    34021: 'RcimEngineError_MessageNotRegistered',
    34025: 'RcimEngineError_MessageExpandConversationTypeNotMatch',
    34022: 'RcimEngineError_InvalidArgumentUltraGroupNotSupport',
    34105: 'RcimEngineError_InvalidArgumentAppKey',
    34202: 'RcimEngineError_InvalidArgumentTimestamp',
    34205: 'RcimEngineError_InvalidArgumentMessageContent',
    34206: 'RcimEngineError_InvalidArgumentMessageVec',
    34209: 'RcimEngineError_InvalidArgumentConversationType',
    34210: 'RcimEngineError_InvalidArgumentTargetId',
    34220: 'RcimEngineError_InvalidParameterMessageExpansion',
    34211: 'RcimEngineError_InvalidArgumentChannelId',
    34223: 'RcimEngineError_InvalidArgumentContentNotMedia',
    33201: 'RcimEngineError_InvalidArgumentFileNameEmpty',
    34224: 'RcimEngineError_InvalidArgumentTimeString',
    34225: 'RcimEngineError_InvalidEnumOutOfRange',
    34228: 'RcimEngineError_InvalidArgumentPushNotificationMuteLevel',
    34229: 'RcimEngineError_InvalidArgumentMessageIdVec',
    34232: 'RcimEngineError_InvalidArgumentCount',
    34234: 'RcimEngineError_InvalidArgumentMediaLocalPath',
    34235: 'RcimEngineError_InvalidArgumentMediaUrl',
    34243: 'RcimEngineError_InvalidArgumentMessage',
    34244: 'RcimEngineError_InvalidArgumentSentStatus',
    34260: 'RcimEngineError_ChatroomKvInvalidKey',
    34261: 'RcimEngineError_ChatroomKvInvalidKeyVec',
    34262: 'RcimEngineError_ChatroomKvInvalidValue',
    34263: 'RcimEngineError_ChatroomKvInvalidKeyValueVec',
    34267: 'RcimEngineError_InvalidArgumentMessageDirectionEmpty',
    34271: 'RcimEngineError_InvalidArgumentObjectName',
    34279: 'RcimEngineError_InvalidArgumentLimit',
    34280: 'RcimEngineError_InvalidArgumentMessageDirection',
    34283: 'RcimEngineError_InvalidArgumentSpanMinutes',
    34284: 'RcimEngineError_InvalidArgumentConversationTypeVec',
    34286: 'RcimEngineError_InvalidArgumentNaviUrl',
    34287: 'RcimEngineError_InvalidArgumentConversationIdentifierVec',
    34296: 'RcimEngineError_DirectionalMessageNotSupport',
    34297: 'RcimEngineError_MessageDestructing',
    23298: 'RcimEngineError_MessageNotDestructing',
    34230: 'RcimEngineError_InvalidParameterReceivedStatus',
    34214: 'RcimEngineError_InvalidParameterUserId',
    34215: 'RcimEngineError_InvalidParameterUserList',
    34301: 'RcimEngineError_DatabaseNotOpened',
    34302: 'RcimEngineError_DatabaseOpenFailed',
    34303: 'RcimEngineError_DatabaseIOError',
    34304: 'RcimEngineError_DatabaseTargetNotFound',
    34305: 'RcimEngineError_NetDataParserFailed',
    34316: 'RcimEngineError_DatabaseThreadError',
    34400: 'RcimEngineError_EngineDropped',
    34002: 'RcimEngineError_SightMsgDurationLimit',
    34401: 'RcimEngineError_InvalidArgumentEngineSync',
    34402: 'RcimEngineError_InvalidArgumentEngineBuilder',
    34403: 'RcimEngineError_InvalidArgumentDeviceId',
    34404: 'RcimEngineError_InvalidArgumentPackageName',
    34405: 'RcimEngineError_InvalidArgumentSdkVersion',
    34406: 'RcimEngineError_InvalidArgumentFileStoragePath',
    34407: 'RcimEngineError_InvalidArgumentToken',
    34408: 'RcimEngineError_InvalidArgumentMessageId',
    34409: 'RcimEngineError_InvalidArgumentMessageType',
    34410: 'RcimEngineError_InvalidArgumentNotMediaMessage',
    34411: 'RcimEngineError_InvalidArgumentUserIdEmpty',
    34413: 'RcimEngineError_InvalidArgumentAudioDuration',
    34414: 'RcimEngineError_InvalidArgumentLogInfo',
    34415: 'RcimEngineError_InvalidArgumentEngineBuilderParam',
    34416: 'RcimEngineError_InvalidArgumentDeviceModel',
    34417: 'RcimEngineError_InvalidArgumentDeviceManufacturer',
    34418: 'RcimEngineError_InvalidArgumentPushTokenVec',
    34419: 'RcimEngineError_InvalidArgumentPushType',
    34420: 'RcimEngineError_InvalidArgumentPushToken',
    34421: 'RcimEngineError_InvalidArgumentSenderId',
    34422: 'RcimEngineError_InvalidArgumentPushNotificationMuteLevelVec',
    34423: 'RcimEngineError_InvalidArgumentConnectionStatus',
    34424: 'RcimEngineError_InvalidArgumentVersion',
    34425: 'RcimEngineError_InvalidArgumentOsVersion',
    34426: 'RcimEngineError_InvalidArgumentAppVersion',
    34427: 'RcimEngineError_InvalidArgumentStatisticUrl',
    34428: 'RcimEngineError_InvalidArgumentDraft',
    34429: 'RcimEngineError_InvalidArgumentKeyword',
    34430: 'RcimEngineError_InvalidArgumentOffset',
    34431: 'RcimEngineError_InvalidArgumentObjectNameVec',
    34432: 'RcimEngineError_InvalidArgumentTimeInterval',
    34433: 'RcimEngineError_InvalidArgumentTimeoutSeconds',
    34434: 'RcimEngineError_InvalidArgumentDestructDuration',
    34435: 'RcimEngineError_InvalidArgumentUniqueId',
    34436: 'RcimEngineError_InvalidArgumentOutUniqueId',
    34437: 'RcimEngineError_InvalidArgumentOutUserId',
    34438: 'RcimEngineError_InvalidArgumentExtra',
    36001: 'RcimEngineError_InvalidArgumentChatroomId',
    36002: 'RcimEngineError_InvalidArgumentRtcMethodName',
    36003: 'RcimEngineError_InvalidArgumentRtcKey',
    36004: 'RcimEngineError_InvalidArgumentRtcValue',
    40001: 'RcimEngineError_CallNotInRoom',
    40002: 'RcimEngineError_CallInternalError',
    40003: 'RcimEngineError_CallHasNoRoom',
    40004: 'RcimEngineError_CallInvalidUserId',
    40005: 'RcimEngineError_CallLimitError',
    40006: 'RcimEngineError_CallParamError',
    40007: 'RcimEngineError_CallTokenError',
    40008: 'RcimEngineError_CallDbError',
    40009: 'RcimEngineError_CallJsonError',
    40010: 'RcimEngineError_CallNotOpen',
    40011: 'RcimEngineError_CallRoomTypeError',
    40012: 'RcimEngineError_CallNoAuthUser',
    40015: 'RcimEngineError_CallHasNoConfigMcuAddress',
    40016: 'RcimEngineError_CallNotAllowVideoBroadcast',
    40017: 'RcimEngineError_CallNotAllowAudioBroadcast',
    40018: 'RcimEngineError_CallGetTokenError',
    40021: 'RcimEngineError_CallUserIsBlocked',
    40022: 'RcimEngineError_CallInviteRoomNotExist',
    40023: 'RcimEngineError_CallInviteUserNotInRoom',
    40024: 'RcimEngineError_CallInviteInProgress',
    40025: 'RcimEngineError_CallCancelInviteNotProgress',
    40026: 'RcimEngineError_CallAnswerInviteNotProgress',
    40027: 'RcimEngineError_CallAnswerInviteTimeout',
    40028: 'RcimEngineError_CallPingNotProgress',
    40029: 'RcimEngineError_CallRoomAlreadyExist',
    40030: 'RcimEngineError_CallRoomTypeNotSupport',
    40031: 'RcimEngineError_CallIdentityChangeTypeError',
    40032: 'RcimEngineError_CallAlreadyJoinRoom',
    40033: 'RcimEngineError_CallNotAllowCrossApp',
    40034: 'RcimEngineError_CallUserNotAllowedForRtc',
    40130: 'RcimEngineError_CallConcurrentLimitError',
    40131: 'RcimEngineError_CallExpiredError',
    41000: 'RcimEngineError_CallplusUnknownError',
    41001: 'RcimEngineError_CallplusDbError',
    41002: 'RcimEngineError_CallplusJsonError',
    41003: 'RcimEngineError_CallplusInvalidJsonFormat',
    41004: 'RcimEngineError_CallplusMissingParameters',
    41005: 'RcimEngineError_CallplusOperationNotPermitted',
    41006: 'RcimEngineError_CallplusCircuitBreakerOpen',
    41007: 'RcimEngineError_CallplusMethodNotImplement',
    41008: 'RcimEngineError_CallplusCallingUserNotRegistCallServer',
    41009: 'RcimEngineError_CallplusNotSupportNewCall',
    41010: 'RcimEngineError_CallplusCallNotExist',
    41011: 'RcimEngineError_CallplusSingleCallOverload',
    41012: 'RcimEngineError_CallplusGroupCallOverload',
    41013: 'RcimEngineError_CallplusOperationHasExpired',
    41014: 'RcimEngineError_CallplusDeviceHasCalling',
    41015: 'RcimEngineError_CallplusCallUserNotInCall',
    41016: 'RcimEngineError_CallplusDataHasExpired',
    41018: 'RcimEngineError_CallplusStreamReadyTimeInvalid',
    41019: 'RcimEngineError_CallplusCallNotSelf',
    41020: 'RcimEngineError_CallplusStateNotExist',
    41021: 'RcimEngineError_CallplusHangupNotAllowed',
    41022: 'RcimEngineError_CallplusAcceptNotAllowed',
    41025: 'RcimEngineError_CallplusOperationNotAllowed',
    41100: 'RcimEngineError_CallplusTransactionNotExist',
    41101: 'RcimEngineError_CallplusMediaTypeSwitching',
    41150: 'RcimEngineError_CallplusAudioToVideoCancel',
    41151: 'RcimEngineError_CallplusVideoToAudioNoRequired',
    41152: 'RcimEngineError_CallplusAudioToVideoNoRequired',
    41200: 'RcimEngineError_CallplusNoCompensationData',
    99999: 'RcimEngineError_NotSupportedYet',
}
RcimEngineError_Success = 0
RcimEngineError_RejectedByBlackList = 405
RcimEngineError_NotWhitelisted = 407
RcimEngineError_ForbiddenInPrivateChat = 20106
RcimEngineError_ConversationNotSupportMessage = 20109
RcimEngineError_MessageSendOverFrequency = 20604
RcimEngineError_RequestOverFrequency = 20607
RcimEngineError_MessageIncludeSensitiveWord = 21501
RcimEngineError_MessageReplacedSensitiveWord = 21502
RcimEngineError_NotInGroup = 22406
RcimEngineError_ForbiddenInGroupChat = 22408
RcimEngineError_ForbiddenInChatroom = 23408
RcimEngineError_ChatroomKicked = 23409
RcimEngineError_ChatroomNotExist = 23410
RcimEngineError_ChatroomIsFull = 23411
RcimEngineError_NotInChatroom = 23406
RcimEngineError_GetUserError = 23407
RcimEngineError_ChatroomInvalidParameter = 23412
RcimEngineError_QueryChatroomHistoryError = 23413
RcimEngineError_RoamingServiceUnavailableChatroom = 23414
RcimEngineError_ChatroomKvCountExceed = 23423
RcimEngineError_ChatroomKvOverwriteInvalidKey = 23424
RcimEngineError_ChatroomKvCallAPIExceed = 23425
RcimEngineError_ChatroomKvStoreUnavailable = 23426
RcimEngineError_ChatroomKvNotExist = 23427
RcimEngineError_ChatroomKvNotAllSuccess = 23428
RcimEngineError_ChatroomKvLimit = 23429
RcimEngineError_ChatroomKvConcurrentError = 23431
RcimEngineError_RecallParameterInvalid = 25101
RcimEngineError_MessageStorageServiceUnavailable = 25102
RcimEngineError_RecallMessageUserInvalid = 25107
RcimEngineError_PushSettingParameterInvalid = 26001
RcimEngineError_SettingSyncFailed = 26002
RcimEngineError_InvalidArgumentMessageUid = 26009
RcimEngineError_RequestUploadTokenSizeError = 26107
RcimEngineError_InvalidPublicService = 29201
RcimEngineError_ConnectionClosed = 30001
RcimEngineError_ConnectionClosing = 30027
RcimEngineError_SocketRecvTimeout = 30003
RcimEngineError_NaviReqFailed = 30004
RcimEngineError_NaviReqTimeout = 30005
RcimEngineError_MsgSizeOutOfLimit = 30016
RcimEngineError_SocketSendTimeout = 30022
RcimEngineError_NaviRespTokenIncorrect = 30024
RcimEngineError_NaviLicenseMismatch = 30026
RcimEngineError_HttpReqFailed = 34026
RcimEngineError_HttpReqTimeout = 34027
RcimEngineError_ConnectIllegalProtocolVersion = 31001
RcimEngineError_ConnectIdReject = 31002
RcimEngineError_ConnectPlatformUnavailable = 31003
RcimEngineError_ConnectTokenIncorrect = 31004
RcimEngineError_ConnectNotAuthorized = 31005
RcimEngineError_ConnectRedirect = 31006
RcimEngineError_ConnectPackageNameInvalid = 31007
RcimEngineError_ConnectAppBlockOrDelete = 31008
RcimEngineError_ConnectUserBlocked = 31009
RcimEngineError_DisconnectUserKicked = 31010
RcimEngineError_DisconnectUserBlocked = 31011
RcimEngineError_DisconnectUserLogout = 31012
RcimEngineError_SocketConnectionFailed = 31014
RcimEngineError_SocketShutdownFailed = 31015
RcimEngineError_ConnectionCancel = 31016
RcimEngineError_ConnectTokenExpired = 31020
RcimEngineError_ConnectDeviceError = 31021
RcimEngineError_ConnectHostnameError = 31022
RcimEngineError_ConnectOtherDeviceLogin = 31023
RcimEngineError_ConnectConcurrentLimitError = 31024
RcimEngineError_ConnectClusterError = 31025
RcimEngineError_ConnectAppAuthFailed = 31026
RcimEngineError_ConnectOneTimePasswordUsed = 31027
RcimEngineError_ConnectPlatformError = 31028
RcimEngineError_ConnectUserDeleteAccount = 31029
RcimEngineError_ConnectLicenseExpired = 31030
RcimEngineError_KvStoreNotOpened = 31510
RcimEngineError_KvStoreOpenFailed = 31511
RcimEngineError_KvStoreIOError = 31512
RcimEngineError_KvStoreSerializationError = 31513
RcimEngineError_JsonParserFailed = 31610
RcimEngineError_ImageFormatError = 31611
RcimEngineError_RequestUploadTokenError = 31612
RcimEngineError_GetUploadTokenError = 31613
RcimEngineError_SightMessageCompressError = 31614
RcimEngineError_RequestCanceled = 33200
RcimEngineError_DownloadRequestExist = 33202
RcimEngineError_RequestPaused = 33204
RcimEngineError_DownloadTaskNotExist = 33205
RcimEngineError_UploadTaskNotExist = 33206
RcimEngineError_MediaMessageHandlerError = 33207
RcimEngineError_ConnectRefused = 32061
RcimEngineError_MessageSavedError = 33000
RcimEngineError_ConnectionInProcess = 33006
RcimEngineError_CloudStorageForHistoryMessageDisable = 33007
RcimEngineError_ConnectionExists = 34001
RcimEngineError_GifMessageSizeOutOfLimit = 34003
RcimEngineError_ConnectionTimeout = 34006
RcimEngineError_MessageCantExpand = 34008
RcimEngineError_MessageExpansionSizeLimitExceed = 34010
RcimEngineError_UploadMediaFailed = 34011
RcimEngineError_GroupReadReceiptVersionNotSupport = 34014
RcimEngineError_UserSettingUnavailable = 34016
RcimEngineError_MessageNotRegistered = 34021
RcimEngineError_MessageExpandConversationTypeNotMatch = 34025
RcimEngineError_InvalidArgumentUltraGroupNotSupport = 34022
RcimEngineError_InvalidArgumentAppKey = 34105
RcimEngineError_InvalidArgumentTimestamp = 34202
RcimEngineError_InvalidArgumentMessageContent = 34205
RcimEngineError_InvalidArgumentMessageVec = 34206
RcimEngineError_InvalidArgumentConversationType = 34209
RcimEngineError_InvalidArgumentTargetId = 34210
RcimEngineError_InvalidParameterMessageExpansion = 34220
RcimEngineError_InvalidArgumentChannelId = 34211
RcimEngineError_InvalidArgumentContentNotMedia = 34223
RcimEngineError_InvalidArgumentFileNameEmpty = 33201
RcimEngineError_InvalidArgumentTimeString = 34224
RcimEngineError_InvalidEnumOutOfRange = 34225
RcimEngineError_InvalidArgumentPushNotificationMuteLevel = 34228
RcimEngineError_InvalidArgumentMessageIdVec = 34229
RcimEngineError_InvalidArgumentCount = 34232
RcimEngineError_InvalidArgumentMediaLocalPath = 34234
RcimEngineError_InvalidArgumentMediaUrl = 34235
RcimEngineError_InvalidArgumentMessage = 34243
RcimEngineError_InvalidArgumentSentStatus = 34244
RcimEngineError_ChatroomKvInvalidKey = 34260
RcimEngineError_ChatroomKvInvalidKeyVec = 34261
RcimEngineError_ChatroomKvInvalidValue = 34262
RcimEngineError_ChatroomKvInvalidKeyValueVec = 34263
RcimEngineError_InvalidArgumentMessageDirectionEmpty = 34267
RcimEngineError_InvalidArgumentObjectName = 34271
RcimEngineError_InvalidArgumentLimit = 34279
RcimEngineError_InvalidArgumentMessageDirection = 34280
RcimEngineError_InvalidArgumentSpanMinutes = 34283
RcimEngineError_InvalidArgumentConversationTypeVec = 34284
RcimEngineError_InvalidArgumentNaviUrl = 34286
RcimEngineError_InvalidArgumentConversationIdentifierVec = 34287
RcimEngineError_DirectionalMessageNotSupport = 34296
RcimEngineError_MessageDestructing = 34297
RcimEngineError_MessageNotDestructing = 23298
RcimEngineError_InvalidParameterReceivedStatus = 34230
RcimEngineError_InvalidParameterUserId = 34214
RcimEngineError_InvalidParameterUserList = 34215
RcimEngineError_DatabaseNotOpened = 34301
RcimEngineError_DatabaseOpenFailed = 34302
RcimEngineError_DatabaseIOError = 34303
RcimEngineError_DatabaseTargetNotFound = 34304
RcimEngineError_NetDataParserFailed = 34305
RcimEngineError_DatabaseThreadError = 34316
RcimEngineError_EngineDropped = 34400
RcimEngineError_SightMsgDurationLimit = 34002
RcimEngineError_InvalidArgumentEngineSync = 34401
RcimEngineError_InvalidArgumentEngineBuilder = 34402
RcimEngineError_InvalidArgumentDeviceId = 34403
RcimEngineError_InvalidArgumentPackageName = 34404
RcimEngineError_InvalidArgumentSdkVersion = 34405
RcimEngineError_InvalidArgumentFileStoragePath = 34406
RcimEngineError_InvalidArgumentToken = 34407
RcimEngineError_InvalidArgumentMessageId = 34408
RcimEngineError_InvalidArgumentMessageType = 34409
RcimEngineError_InvalidArgumentNotMediaMessage = 34410
RcimEngineError_InvalidArgumentUserIdEmpty = 34411
RcimEngineError_InvalidArgumentAudioDuration = 34413
RcimEngineError_InvalidArgumentLogInfo = 34414
RcimEngineError_InvalidArgumentEngineBuilderParam = 34415
RcimEngineError_InvalidArgumentDeviceModel = 34416
RcimEngineError_InvalidArgumentDeviceManufacturer = 34417
RcimEngineError_InvalidArgumentPushTokenVec = 34418
RcimEngineError_InvalidArgumentPushType = 34419
RcimEngineError_InvalidArgumentPushToken = 34420
RcimEngineError_InvalidArgumentSenderId = 34421
RcimEngineError_InvalidArgumentPushNotificationMuteLevelVec = 34422
RcimEngineError_InvalidArgumentConnectionStatus = 34423
RcimEngineError_InvalidArgumentVersion = 34424
RcimEngineError_InvalidArgumentOsVersion = 34425
RcimEngineError_InvalidArgumentAppVersion = 34426
RcimEngineError_InvalidArgumentStatisticUrl = 34427
RcimEngineError_InvalidArgumentDraft = 34428
RcimEngineError_InvalidArgumentKeyword = 34429
RcimEngineError_InvalidArgumentOffset = 34430
RcimEngineError_InvalidArgumentObjectNameVec = 34431
RcimEngineError_InvalidArgumentTimeInterval = 34432
RcimEngineError_InvalidArgumentTimeoutSeconds = 34433
RcimEngineError_InvalidArgumentDestructDuration = 34434
RcimEngineError_InvalidArgumentUniqueId = 34435
RcimEngineError_InvalidArgumentOutUniqueId = 34436
RcimEngineError_InvalidArgumentOutUserId = 34437
RcimEngineError_InvalidArgumentExtra = 34438
RcimEngineError_InvalidArgumentChatroomId = 36001
RcimEngineError_InvalidArgumentRtcMethodName = 36002
RcimEngineError_InvalidArgumentRtcKey = 36003
RcimEngineError_InvalidArgumentRtcValue = 36004
RcimEngineError_CallNotInRoom = 40001
RcimEngineError_CallInternalError = 40002
RcimEngineError_CallHasNoRoom = 40003
RcimEngineError_CallInvalidUserId = 40004
RcimEngineError_CallLimitError = 40005
RcimEngineError_CallParamError = 40006
RcimEngineError_CallTokenError = 40007
RcimEngineError_CallDbError = 40008
RcimEngineError_CallJsonError = 40009
RcimEngineError_CallNotOpen = 40010
RcimEngineError_CallRoomTypeError = 40011
RcimEngineError_CallNoAuthUser = 40012
RcimEngineError_CallHasNoConfigMcuAddress = 40015
RcimEngineError_CallNotAllowVideoBroadcast = 40016
RcimEngineError_CallNotAllowAudioBroadcast = 40017
RcimEngineError_CallGetTokenError = 40018
RcimEngineError_CallUserIsBlocked = 40021
RcimEngineError_CallInviteRoomNotExist = 40022
RcimEngineError_CallInviteUserNotInRoom = 40023
RcimEngineError_CallInviteInProgress = 40024
RcimEngineError_CallCancelInviteNotProgress = 40025
RcimEngineError_CallAnswerInviteNotProgress = 40026
RcimEngineError_CallAnswerInviteTimeout = 40027
RcimEngineError_CallPingNotProgress = 40028
RcimEngineError_CallRoomAlreadyExist = 40029
RcimEngineError_CallRoomTypeNotSupport = 40030
RcimEngineError_CallIdentityChangeTypeError = 40031
RcimEngineError_CallAlreadyJoinRoom = 40032
RcimEngineError_CallNotAllowCrossApp = 40033
RcimEngineError_CallUserNotAllowedForRtc = 40034
RcimEngineError_CallConcurrentLimitError = 40130
RcimEngineError_CallExpiredError = 40131
RcimEngineError_CallplusUnknownError = 41000
RcimEngineError_CallplusDbError = 41001
RcimEngineError_CallplusJsonError = 41002
RcimEngineError_CallplusInvalidJsonFormat = 41003
RcimEngineError_CallplusMissingParameters = 41004
RcimEngineError_CallplusOperationNotPermitted = 41005
RcimEngineError_CallplusCircuitBreakerOpen = 41006
RcimEngineError_CallplusMethodNotImplement = 41007
RcimEngineError_CallplusCallingUserNotRegistCallServer = 41008
RcimEngineError_CallplusNotSupportNewCall = 41009
RcimEngineError_CallplusCallNotExist = 41010
RcimEngineError_CallplusSingleCallOverload = 41011
RcimEngineError_CallplusGroupCallOverload = 41012
RcimEngineError_CallplusOperationHasExpired = 41013
RcimEngineError_CallplusDeviceHasCalling = 41014
RcimEngineError_CallplusCallUserNotInCall = 41015
RcimEngineError_CallplusDataHasExpired = 41016
RcimEngineError_CallplusStreamReadyTimeInvalid = 41018
RcimEngineError_CallplusCallNotSelf = 41019
RcimEngineError_CallplusStateNotExist = 41020
RcimEngineError_CallplusHangupNotAllowed = 41021
RcimEngineError_CallplusAcceptNotAllowed = 41022
RcimEngineError_CallplusOperationNotAllowed = 41025
RcimEngineError_CallplusTransactionNotExist = 41100
RcimEngineError_CallplusMediaTypeSwitching = 41101
RcimEngineError_CallplusAudioToVideoCancel = 41150
RcimEngineError_CallplusVideoToAudioNoRequired = 41151
RcimEngineError_CallplusAudioToVideoNoRequired = 41152
RcimEngineError_CallplusNoCompensationData = 41200
RcimEngineError_NotSupportedYet = 99999
RcimEngineError = ctypes.c_uint32 # enum

# values for enumeration 'RcimLogLevel'
RcimLogLevel__enumvalues = {
    0: 'RcimLogLevel_None',
    1: 'RcimLogLevel_Error',
    2: 'RcimLogLevel_Warn',
    3: 'RcimLogLevel_Info',
    4: 'RcimLogLevel_Debug',
}
RcimLogLevel_None = 0
RcimLogLevel_Error = 1
RcimLogLevel_Warn = 2
RcimLogLevel_Info = 3
RcimLogLevel_Debug = 4
RcimLogLevel = ctypes.c_uint32 # enum

# values for enumeration 'RcimLogSource'
RcimLogSource__enumvalues = {
    0: 'RcimLogSource_RUST',
    1: 'RcimLogSource_FFI',
    2: 'RcimLogSource_IMLib',
    3: 'RcimLogSource_IMKit',
    4: 'RcimLogSource_RTCLib',
    5: 'RcimLogSource_CallLib',
    6: 'RcimLogSource_CallPlus',
}
RcimLogSource_RUST = 0
RcimLogSource_FFI = 1
RcimLogSource_IMLib = 2
RcimLogSource_IMKit = 3
RcimLogSource_RTCLib = 4
RcimLogSource_CallLib = 5
RcimLogSource_CallPlus = 6
RcimLogSource = ctypes.c_uint32 # enum

# values for enumeration 'RcimLogType'
RcimLogType__enumvalues = {
    0: 'RcimLogType_IM',
    1: 'RcimLogType_RTC',
}
RcimLogType_IM = 0
RcimLogType_RTC = 1
RcimLogType = ctypes.c_uint32 # enum

# values for enumeration 'RcimMediaHandlerError'
RcimMediaHandlerError__enumvalues = {
    0: 'RcimMediaHandlerError_Success',
    1: 'RcimMediaHandlerError_Canceled',
    2: 'RcimMediaHandlerError_Paused',
    3: 'RcimMediaHandlerError_Failed',
}
RcimMediaHandlerError_Success = 0
RcimMediaHandlerError_Canceled = 1
RcimMediaHandlerError_Paused = 2
RcimMediaHandlerError_Failed = 3
RcimMediaHandlerError = ctypes.c_uint32 # enum

# values for enumeration 'RcimMessageBlockSourceType'
RcimMessageBlockSourceType__enumvalues = {
    0: 'RcimMessageBlockSourceType_Default',
    1: 'RcimMessageBlockSourceType_Extension',
    2: 'RcimMessageBlockSourceType_Modification',
}
RcimMessageBlockSourceType_Default = 0
RcimMessageBlockSourceType_Extension = 1
RcimMessageBlockSourceType_Modification = 2
RcimMessageBlockSourceType = ctypes.c_uint32 # enum

# values for enumeration 'RcimMessageBlockType'
RcimMessageBlockType__enumvalues = {
    0: 'RcimMessageBlockType_None',
    1: 'RcimMessageBlockType_BlockGlobal',
    2: 'RcimMessageBlockType_BlockCustom',
    3: 'RcimMessageBlockType_BlockThirdParty',
}
RcimMessageBlockType_None = 0
RcimMessageBlockType_BlockGlobal = 1
RcimMessageBlockType_BlockCustom = 2
RcimMessageBlockType_BlockThirdParty = 3
RcimMessageBlockType = ctypes.c_uint32 # enum

# values for enumeration 'RcimMessageDirection'
RcimMessageDirection__enumvalues = {
    1: 'RcimMessageDirection_Send',
    2: 'RcimMessageDirection_Receive',
}
RcimMessageDirection_Send = 1
RcimMessageDirection_Receive = 2
RcimMessageDirection = ctypes.c_uint32 # enum

# values for enumeration 'RcimMessageFlag'
RcimMessageFlag__enumvalues = {
    0: 'RcimMessageFlag_None',
    1: 'RcimMessageFlag_Save',
    3: 'RcimMessageFlag_Count',
    16: 'RcimMessageFlag_Status',
}
RcimMessageFlag_None = 0
RcimMessageFlag_Save = 1
RcimMessageFlag_Count = 3
RcimMessageFlag_Status = 16
RcimMessageFlag = ctypes.c_uint32 # enum

# values for enumeration 'RcimNetworkType'
RcimNetworkType__enumvalues = {
    0: 'RcimNetworkType_None',
    1: 'RcimNetworkType_Wifi',
    2: 'RcimNetworkType_Wired',
    3: 'RcimNetworkType_Cellular2G',
    4: 'RcimNetworkType_Cellular3G',
    5: 'RcimNetworkType_Cellular4G',
    6: 'RcimNetworkType_Cellular5G',
}
RcimNetworkType_None = 0
RcimNetworkType_Wifi = 1
RcimNetworkType_Wired = 2
RcimNetworkType_Cellular2G = 3
RcimNetworkType_Cellular3G = 4
RcimNetworkType_Cellular4G = 5
RcimNetworkType_Cellular5G = 6
RcimNetworkType = ctypes.c_uint32 # enum

# values for enumeration 'RcimOrder'
RcimOrder__enumvalues = {
    0: 'RcimOrder_Descending',
    1: 'RcimOrder_Ascending',
}
RcimOrder_Descending = 0
RcimOrder_Ascending = 1
RcimOrder = ctypes.c_uint32 # enum

# values for enumeration 'RcimPlatform'
RcimPlatform__enumvalues = {
    0: 'RcimPlatform_Android',
    1: 'RcimPlatform_IOS',
    2: 'RcimPlatform_HarmonyOS',
    3: 'RcimPlatform_Windows',
    4: 'RcimPlatform_MacOS',
    5: 'RcimPlatform_Linux',
    6: 'RcimPlatform_Electron',
    7: 'RcimPlatform_Web',
    127: 'RcimPlatform_Unknown',
}
RcimPlatform_Android = 0
RcimPlatform_IOS = 1
RcimPlatform_HarmonyOS = 2
RcimPlatform_Windows = 3
RcimPlatform_MacOS = 4
RcimPlatform_Linux = 5
RcimPlatform_Electron = 6
RcimPlatform_Web = 7
RcimPlatform_Unknown = 127
RcimPlatform = ctypes.c_uint32 # enum

# values for enumeration 'RcimPublicServiceMenuItemType'
RcimPublicServiceMenuItemType__enumvalues = {
    0: 'RcimPublicServiceMenuItemType_Group',
    1: 'RcimPublicServiceMenuItemType_View',
    2: 'RcimPublicServiceMenuItemType_Click',
}
RcimPublicServiceMenuItemType_Group = 0
RcimPublicServiceMenuItemType_View = 1
RcimPublicServiceMenuItemType_Click = 2
RcimPublicServiceMenuItemType = ctypes.c_uint32 # enum

# values for enumeration 'RcimPushNotificationMuteLevel'
RcimPushNotificationMuteLevel__enumvalues = {
    -1: 'RcimPushNotificationMuteLevel_All',
    0: 'RcimPushNotificationMuteLevel_Default',
    1: 'RcimPushNotificationMuteLevel_Mention',
    2: 'RcimPushNotificationMuteLevel_MentionUsers',
    4: 'RcimPushNotificationMuteLevel_MentionAll',
    5: 'RcimPushNotificationMuteLevel_Blocked',
}
RcimPushNotificationMuteLevel_All = -1
RcimPushNotificationMuteLevel_Default = 0
RcimPushNotificationMuteLevel_Mention = 1
RcimPushNotificationMuteLevel_MentionUsers = 2
RcimPushNotificationMuteLevel_MentionAll = 4
RcimPushNotificationMuteLevel_Blocked = 5
RcimPushNotificationMuteLevel = ctypes.c_int32 # enum

# values for enumeration 'RcimSentStatus'
RcimSentStatus__enumvalues = {
    10: 'RcimSentStatus_SENDING',
    20: 'RcimSentStatus_FAILED',
    30: 'RcimSentStatus_SENT',
    40: 'RcimSentStatus_RECEIVED',
    50: 'RcimSentStatus_READ',
    60: 'RcimSentStatus_DESTROYED',
    70: 'RcimSentStatus_CANCELED',
}
RcimSentStatus_SENDING = 10
RcimSentStatus_FAILED = 20
RcimSentStatus_SENT = 30
RcimSentStatus_RECEIVED = 40
RcimSentStatus_READ = 50
RcimSentStatus_DESTROYED = 60
RcimSentStatus_CANCELED = 70
RcimSentStatus = ctypes.c_uint32 # enum
class struct_RcimEngineBuilder(Structure):
    pass

RcimEngineBuilder = struct_RcimEngineBuilder
class struct_RcimEngineSync(Structure):
    pass

RcimEngineSync = struct_RcimEngineSync
class struct_RcimSDKVersion(Structure):
    pass

struct_RcimSDKVersion._pack_ = 1 # source:False
struct_RcimSDKVersion._fields_ = [
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('version', ctypes.POINTER(ctypes.c_char)),
]

RcimSDKVersion = struct_RcimSDKVersion
class struct_RcimEngineBuilderParam(Structure):
    pass

struct_RcimEngineBuilderParam._pack_ = 1 # source:False
struct_RcimEngineBuilderParam._fields_ = [
    ('app_key', ctypes.POINTER(ctypes.c_char)),
    ('platform', RcimPlatform),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('device_id', ctypes.POINTER(ctypes.c_char)),
    ('package_name', ctypes.POINTER(ctypes.c_char)),
    ('imlib_version', ctypes.POINTER(ctypes.c_char)),
    ('device_model', ctypes.POINTER(ctypes.c_char)),
    ('device_manufacturer', ctypes.POINTER(ctypes.c_char)),
    ('os_version', ctypes.POINTER(ctypes.c_char)),
    ('sdk_version_vec', ctypes.POINTER(struct_RcimSDKVersion)),
    ('sdk_version_vec_len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('app_version', ctypes.POINTER(ctypes.c_char)),
]

RcimEngineBuilderParam = struct_RcimEngineBuilderParam
RcimDatabaseStatusLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimDatabaseStatus)
class struct_RcimPushTokenInfo(Structure):
    pass

struct_RcimPushTokenInfo._pack_ = 1 # source:False
struct_RcimPushTokenInfo._fields_ = [
    ('push_type', ctypes.POINTER(ctypes.c_char)),
    ('push_token', ctypes.POINTER(ctypes.c_char)),
]

RcimPushTokenInfo = struct_RcimPushTokenInfo
RcimConnectionStatusLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimConnectionStatus)
RcimConnectCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char))
RcimEngineErrorCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError)
class struct_RcimReceivedStatus(Structure):
    pass

struct_RcimReceivedStatus._pack_ = 1 # source:False
struct_RcimReceivedStatus._fields_ = [
    ('is_read', ctypes.c_bool),
    ('is_listened', ctypes.c_bool),
    ('is_download', ctypes.c_bool),
    ('is_retrieved', ctypes.c_bool),
    ('is_multiple_received', ctypes.c_bool),
]

RcimReceivedStatus = struct_RcimReceivedStatus
class struct_RcimReadReceiptUserInfo(Structure):
    pass

struct_RcimReadReceiptUserInfo._pack_ = 1 # source:False
struct_RcimReadReceiptUserInfo._fields_ = [
    ('sender_id', ctypes.POINTER(ctypes.c_char)),
    ('timestamp', ctypes.c_uint64),
]

RcimReadReceiptUserInfo = struct_RcimReadReceiptUserInfo
class struct_RcimReadReceiptInfo(Structure):
    pass

struct_RcimReadReceiptInfo._pack_ = 1 # source:False
struct_RcimReadReceiptInfo._fields_ = [
    ('is_read_receipt_message', ctypes.c_bool),
    ('has_respond', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('respond_user_vec', ctypes.POINTER(struct_RcimReadReceiptUserInfo)),
    ('respond_user_vec_len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

RcimReadReceiptInfo = struct_RcimReadReceiptInfo
class struct_RcimReadReceiptInfoV2(Structure):
    pass

struct_RcimReadReceiptInfoV2._pack_ = 1 # source:False
struct_RcimReadReceiptInfoV2._fields_ = [
    ('has_respond', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('respond_user_vec', ctypes.POINTER(struct_RcimReadReceiptUserInfo)),
    ('respond_user_vec_len', ctypes.c_int32),
    ('read_count', ctypes.c_uint32),
    ('total_count', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

RcimReadReceiptInfoV2 = struct_RcimReadReceiptInfoV2
class struct_RcimIosConfig(Structure):
    pass

struct_RcimIosConfig._pack_ = 1 # source:False
struct_RcimIosConfig._fields_ = [
    ('thread_id', ctypes.POINTER(ctypes.c_char)),
    ('category', ctypes.POINTER(ctypes.c_char)),
    ('apns_collapse_id', ctypes.POINTER(ctypes.c_char)),
    ('rich_media_uri', ctypes.POINTER(ctypes.c_char)),
    ('interruption_level', ctypes.POINTER(ctypes.c_char)),
]

RcimIosConfig = struct_RcimIosConfig
class struct_RcimAndroidConfig(Structure):
    pass

struct_RcimAndroidConfig._pack_ = 1 # source:False
struct_RcimAndroidConfig._fields_ = [
    ('notification_id', ctypes.POINTER(ctypes.c_char)),
    ('mi_channel_id', ctypes.POINTER(ctypes.c_char)),
    ('hw_channel_id', ctypes.POINTER(ctypes.c_char)),
    ('hw_importance', ctypes.POINTER(ctypes.c_char)),
    ('hw_image_url', ctypes.POINTER(ctypes.c_char)),
    ('hw_category', ctypes.POINTER(ctypes.c_char)),
    ('honor_importance', ctypes.POINTER(ctypes.c_char)),
    ('honor_image_url', ctypes.POINTER(ctypes.c_char)),
    ('oppo_channel_id', ctypes.POINTER(ctypes.c_char)),
    ('vivo_category', ctypes.POINTER(ctypes.c_char)),
    ('vivo_type', ctypes.POINTER(ctypes.c_char)),
    ('fcm_channel_id', ctypes.POINTER(ctypes.c_char)),
    ('fcm_collapse_key', ctypes.POINTER(ctypes.c_char)),
    ('fcm_image_url', ctypes.POINTER(ctypes.c_char)),
]

RcimAndroidConfig = struct_RcimAndroidConfig
class struct_RcimHarmonyConfig(Structure):
    pass

struct_RcimHarmonyConfig._pack_ = 1 # source:False
struct_RcimHarmonyConfig._fields_ = [
    ('image_url', ctypes.POINTER(ctypes.c_char)),
    ('category', ctypes.POINTER(ctypes.c_char)),
]

RcimHarmonyConfig = struct_RcimHarmonyConfig
class struct_RcimPushConfig(Structure):
    pass

struct_RcimPushConfig._pack_ = 1 # source:False
struct_RcimPushConfig._fields_ = [
    ('disable_push_title', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('push_title', ctypes.POINTER(ctypes.c_char)),
    ('push_content', ctypes.POINTER(ctypes.c_char)),
    ('push_data', ctypes.POINTER(ctypes.c_char)),
    ('force_show_detail_content', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('ios_config', ctypes.POINTER(struct_RcimIosConfig)),
    ('android_config', ctypes.POINTER(struct_RcimAndroidConfig)),
    ('harmony_config', ctypes.POINTER(struct_RcimHarmonyConfig)),
]

RcimPushConfig = struct_RcimPushConfig
class struct_RcimMessageBox(Structure):
    pass

struct_RcimMessageBox._pack_ = 1 # source:False
struct_RcimMessageBox._fields_ = [
    ('conv_type', RcimConversationType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('target_id', ctypes.POINTER(ctypes.c_char)),
    ('channel_id', ctypes.POINTER(ctypes.c_char)),
    ('message_id', ctypes.c_int64),
    ('direction', RcimMessageDirection),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('sender_id', ctypes.POINTER(ctypes.c_char)),
    ('received_status', ctypes.POINTER(struct_RcimReceivedStatus)),
    ('sent_status', RcimSentStatus),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('received_time', ctypes.c_int64),
    ('sent_time', ctypes.c_int64),
    ('object_name', ctypes.POINTER(ctypes.c_char)),
    ('content', ctypes.POINTER(ctypes.c_char)),
    ('searchable_words', ctypes.POINTER(ctypes.c_char)),
    ('uid', ctypes.POINTER(ctypes.c_char)),
    ('extra', ctypes.POINTER(ctypes.c_char)),
    ('read_receipt_info', ctypes.POINTER(struct_RcimReadReceiptInfo)),
    ('read_receipt_info_v2', ctypes.POINTER(struct_RcimReadReceiptInfoV2)),
    ('is_notification_disabled', ctypes.c_bool),
    ('PADDING_3', ctypes.c_ubyte * 7),
    ('push_config', ctypes.POINTER(struct_RcimPushConfig)),
    ('is_offline', ctypes.c_bool),
    ('is_ext_supported', ctypes.c_bool),
    ('PADDING_4', ctypes.c_ubyte * 6),
    ('ext_content', ctypes.POINTER(ctypes.c_char)),
]

RcimMessageBox = struct_RcimMessageBox
class struct_RcimReceivedInfo(Structure):
    pass

struct_RcimReceivedInfo._pack_ = 1 # source:False
struct_RcimReceivedInfo._fields_ = [
    ('left', ctypes.c_int32),
    ('has_package', ctypes.c_bool),
    ('is_offline', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

RcimReceivedInfo = struct_RcimReceivedInfo
RcimMessageReceivedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(struct_RcimReceivedInfo))
RcimOfflineMessageSyncCompletedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None))
RcimMessageSearchableWordsCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char))
RcimMessageSearchableWordsCbLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char)))
RcimSightCompressCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char))
RcimSightCompressCbLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char)))
class struct_RcimRecallNotificationMessage(Structure):
    pass

struct_RcimRecallNotificationMessage._pack_ = 1 # source:False
struct_RcimRecallNotificationMessage._fields_ = [
    ('base_info', ctypes.POINTER(ctypes.c_char)),
    ('operator_id', ctypes.POINTER(ctypes.c_char)),
    ('recall_time', ctypes.c_int64),
    ('original_object_name', ctypes.POINTER(ctypes.c_char)),
    ('original_content', ctypes.POINTER(ctypes.c_char)),
    ('recall_content', ctypes.POINTER(ctypes.c_char)),
    ('action_time', ctypes.c_int64),
    ('is_admin', ctypes.c_bool),
    ('is_deleted', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

RcimRecallNotificationMessage = struct_RcimRecallNotificationMessage
RcimRecallMessageLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(struct_RcimRecallNotificationMessage))
class struct_RcimMessageBlockInfo(Structure):
    pass

struct_RcimMessageBlockInfo._pack_ = 1 # source:False
struct_RcimMessageBlockInfo._fields_ = [
    ('conv_type', RcimConversationType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('target_id', ctypes.POINTER(ctypes.c_char)),
    ('channel_id', ctypes.POINTER(ctypes.c_char)),
    ('uid', ctypes.POINTER(ctypes.c_char)),
    ('extra', ctypes.POINTER(ctypes.c_char)),
    ('block_type', RcimMessageBlockType),
    ('source_type', RcimMessageBlockSourceType),
    ('source_content', ctypes.POINTER(ctypes.c_char)),
]

RcimMessageBlockInfo = struct_RcimMessageBlockInfo
RcimMessageBlockedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBlockInfo))
class struct_RcimSendMessageOption(Structure):
    pass

struct_RcimSendMessageOption._pack_ = 1 # source:False
struct_RcimSendMessageOption._fields_ = [
    ('is_voip_push', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('user_ids', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
    ('user_ids_len', ctypes.c_int32),
    ('encrypted', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
]

RcimSendMessageOption = struct_RcimSendMessageOption
RcimCodeMessageCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimMessageBox))
RcimMessageCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox))
class struct_RcimSendReadReceiptResponseMessageData(Structure):
    pass

struct_RcimSendReadReceiptResponseMessageData._pack_ = 1 # source:False
struct_RcimSendReadReceiptResponseMessageData._fields_ = [
    ('sender_id', ctypes.POINTER(ctypes.c_char)),
    ('message_uid', ctypes.POINTER(ctypes.c_char)),
]

RcimSendReadReceiptResponseMessageData = struct_RcimSendReadReceiptResponseMessageData
RcimGetMessageListCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimMessageBox), ctypes.c_int32)
RcimMessageNotifyLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox))
RcimReadReceiptRequestLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
RcimReadReceiptResponseLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimReadReceiptUserInfo), ctypes.c_int32)
class struct_RcimReadReceiptV2ReaderInfo(Structure):
    pass

struct_RcimReadReceiptV2ReaderInfo._pack_ = 1 # source:False
struct_RcimReadReceiptV2ReaderInfo._fields_ = [
    ('user_id', ctypes.POINTER(ctypes.c_char)),
    ('read_time', ctypes.c_int64),
]

RcimReadReceiptV2ReaderInfo = struct_RcimReadReceiptV2ReaderInfo
RcimGetReadReceiptV2ReaderListCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.c_uint32, ctypes.POINTER(struct_RcimReadReceiptV2ReaderInfo), ctypes.c_int32)
RcimReadReceiptResponseV2Lsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint32, ctypes.c_uint32)
RcimSendMessageOnProgressCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox), ctypes.c_ubyte)
RcimMediaHandlerProgressCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_int32)
RcimMediaHandlerResultCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimMediaHandlerError, ctypes.POINTER(ctypes.c_char))
RcimMediaMessageHandlerCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(None), ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_int32), ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimMediaHandlerError, ctypes.POINTER(ctypes.c_char)))
RcimDownloadMediaCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char))
RcimDownloadMessageProgressCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_int64, ctypes.c_ubyte)
RcimDownloadFileProgressCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.c_ubyte)
RcimRecallMessageCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimRecallNotificationMessage))
class struct_RcimMessageType(Structure):
    pass

struct_RcimMessageType._pack_ = 1 # source:False
struct_RcimMessageType._fields_ = [
    ('object_name', ctypes.POINTER(ctypes.c_char)),
    ('flag', RcimMessageFlag),
    ('is_media_message', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

RcimMessageType = struct_RcimMessageType
class struct_RcimMessageExpansionKvInfo(Structure):
    pass

struct_RcimMessageExpansionKvInfo._pack_ = 1 # source:False
struct_RcimMessageExpansionKvInfo._fields_ = [
    ('key', ctypes.POINTER(ctypes.c_char)),
    ('value', ctypes.POINTER(ctypes.c_char)),
]

RcimMessageExpansionKvInfo = struct_RcimMessageExpansionKvInfo
RcimMessageExpansionKvUpdateLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageExpansionKvInfo), ctypes.c_int32, ctypes.POINTER(struct_RcimMessageBox))
RcimMessageExpansionKvRemoveLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int32, ctypes.POINTER(struct_RcimMessageBox))
RcimGetBoolCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.c_bool)
RcimMessageDestructingLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox), ctypes.c_int32)
RcimMessageDestructionStopLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimMessageBox))
class struct_RcimConversationStatusChangeItem(Structure):
    pass

struct_RcimConversationStatusChangeItem._pack_ = 1 # source:False
struct_RcimConversationStatusChangeItem._fields_ = [
    ('conv_type', RcimConversationType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('target_id', ctypes.POINTER(ctypes.c_char)),
    ('channel_id', ctypes.POINTER(ctypes.c_char)),
    ('update_time', ctypes.c_int64),
    ('pin_time', ctypes.POINTER(ctypes.c_int64)),
    ('is_pinned', ctypes.POINTER(ctypes.c_bool)),
    ('mute_level', ctypes.POINTER(RcimPushNotificationMuteLevel)),
]

RcimConversationStatusChangeItem = struct_RcimConversationStatusChangeItem
RcimConversationStatusLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimConversationStatusChangeItem), ctypes.c_int32)
class struct_RcimTypingStatus(Structure):
    pass

struct_RcimTypingStatus._pack_ = 1 # source:False
struct_RcimTypingStatus._fields_ = [
    ('user_id', ctypes.POINTER(ctypes.c_char)),
    ('object_name', ctypes.POINTER(ctypes.c_char)),
    ('sent_time', ctypes.c_uint64),
]

RcimTypingStatus = struct_RcimTypingStatus
RcimTypingStatusLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimTypingStatus), ctypes.c_int32)
class struct_RcimConversation(Structure):
    pass

struct_RcimConversation._pack_ = 1 # source:False
struct_RcimConversation._fields_ = [
    ('conv_type', RcimConversationType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('target_id', ctypes.POINTER(ctypes.c_char)),
    ('channel_id', ctypes.POINTER(ctypes.c_char)),
    ('unread_message_count', ctypes.c_int32),
    ('is_pinned', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('last_received_time', ctypes.c_int64),
    ('last_sent_time', ctypes.c_int64),
    ('last_operate_time', ctypes.c_int64),
    ('object_name', ctypes.POINTER(ctypes.c_char)),
    ('sender_user_id', ctypes.POINTER(ctypes.c_char)),
    ('last_message_id', ctypes.c_int64),
    ('last_message_content', ctypes.POINTER(ctypes.c_char)),
    ('draft', ctypes.POINTER(ctypes.c_char)),
    ('mute_level', RcimPushNotificationMuteLevel),
    ('mentioned_count', ctypes.c_int32),
    ('match_count', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
]

RcimConversation = struct_RcimConversation
RcimGetConversationCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimConversation))
RcimGetConversationListCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimConversation), ctypes.c_int32)
class struct_RcimConversationIdentifier(Structure):
    pass

struct_RcimConversationIdentifier._pack_ = 1 # source:False
struct_RcimConversationIdentifier._fields_ = [
    ('conv_type', RcimConversationType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('target_id', ctypes.POINTER(ctypes.c_char)),
    ('channel_id', ctypes.POINTER(ctypes.c_char)),
]

RcimConversationIdentifier = struct_RcimConversationIdentifier
RcimGetLocalConversationMuteLevelCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, RcimPushNotificationMuteLevel)
RcimGetNoDisturbingCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char), ctypes.c_int32, RcimPushNotificationMuteLevel)
RcimGetTextMessageDraftCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char))
RcimGetCountCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.c_int64)
RcimConversationReadStatusLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_int64)
class struct_RcimChatroomJoinedInfo(Structure):
    pass

struct_RcimChatroomJoinedInfo._pack_ = 1 # source:False
struct_RcimChatroomJoinedInfo._fields_ = [
    ('create_time', ctypes.c_int64),
    ('member_count', ctypes.c_int32),
    ('is_all_chatroom_banned', ctypes.c_bool),
    ('is_current_user_banned', ctypes.c_bool),
    ('is_current_chatroom_banned', ctypes.c_bool),
    ('is_current_chatroom_in_whitelist', ctypes.c_bool),
]

RcimChatroomJoinedInfo = struct_RcimChatroomJoinedInfo
RcimChatroomStatusLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char), RcimChatroomStatus, ctypes.POINTER(struct_RcimChatroomJoinedInfo))
class struct_RcimChatroomMemberActionInfo(Structure):
    pass

struct_RcimChatroomMemberActionInfo._pack_ = 1 # source:False
struct_RcimChatroomMemberActionInfo._fields_ = [
    ('user_id', ctypes.POINTER(ctypes.c_char)),
    ('action_type', RcimChatroomMemberActionType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

RcimChatroomMemberActionInfo = struct_RcimChatroomMemberActionInfo
class struct_RcimChatroomMemberChangeInfo(Structure):
    pass

struct_RcimChatroomMemberChangeInfo._pack_ = 1 # source:False
struct_RcimChatroomMemberChangeInfo._fields_ = [
    ('room_id', ctypes.POINTER(ctypes.c_char)),
    ('member_count', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('action_vec', ctypes.POINTER(struct_RcimChatroomMemberActionInfo)),
    ('action_vec_len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

RcimChatroomMemberChangeInfo = struct_RcimChatroomMemberChangeInfo
RcimChatroomMemberChangedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimChatroomMemberChangeInfo))
class struct_RcimChatroomMemberBannedInfo(Structure):
    pass

struct_RcimChatroomMemberBannedInfo._pack_ = 1 # source:False
struct_RcimChatroomMemberBannedInfo._fields_ = [
    ('room_id', ctypes.POINTER(ctypes.c_char)),
    ('event_type', RcimChatroomMemberBannedEventType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('duration_time', ctypes.c_int64),
    ('operate_time', ctypes.c_int64),
    ('user_id_vec', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
    ('user_id_vec_len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('extra', ctypes.POINTER(ctypes.c_char)),
]

RcimChatroomMemberBannedInfo = struct_RcimChatroomMemberBannedInfo
RcimChatroomMemberBannedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimChatroomMemberBannedInfo))
class struct_RcimChatroomMemberBlockedInfo(Structure):
    pass

struct_RcimChatroomMemberBlockedInfo._pack_ = 1 # source:False
struct_RcimChatroomMemberBlockedInfo._fields_ = [
    ('room_id', ctypes.POINTER(ctypes.c_char)),
    ('event_type', RcimChatroomMemberBlockedEventType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('duration_time', ctypes.c_int64),
    ('operate_time', ctypes.c_int64),
    ('user_id_vec', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
    ('user_id_vec_len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('extra', ctypes.POINTER(ctypes.c_char)),
]

RcimChatroomMemberBlockedInfo = struct_RcimChatroomMemberBlockedInfo
RcimChatroomMemberBlockedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimChatroomMemberBlockedInfo))
class struct_RcimChatroomMultiClientSyncInfo(Structure):
    pass

struct_RcimChatroomMultiClientSyncInfo._pack_ = 1 # source:False
struct_RcimChatroomMultiClientSyncInfo._fields_ = [
    ('room_id', ctypes.POINTER(ctypes.c_char)),
    ('event_type', RcimChatroomMultiClientSyncEventType),
    ('quit_type', RcimChatroomMultiClientSyncQuitType),
    ('time', ctypes.c_int64),
    ('extra', ctypes.POINTER(ctypes.c_char)),
]

RcimChatroomMultiClientSyncInfo = struct_RcimChatroomMultiClientSyncInfo
RcimChatroomMultiClientSyncLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimChatroomMultiClientSyncInfo))
RcimJoinChatroomCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimChatroomJoinedInfo))
RcimJoinExistingChatroomCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimChatroomJoinedInfo))
class struct_RcimChatroomUserInfo(Structure):
    pass

struct_RcimChatroomUserInfo._pack_ = 1 # source:False
struct_RcimChatroomUserInfo._fields_ = [
    ('user_id', ctypes.POINTER(ctypes.c_char)),
    ('join_time', ctypes.c_int64),
]

RcimChatroomUserInfo = struct_RcimChatroomUserInfo
class struct_RcimChatroomInfo(Structure):
    pass

struct_RcimChatroomInfo._pack_ = 1 # source:False
struct_RcimChatroomInfo._fields_ = [
    ('room_id', ctypes.POINTER(ctypes.c_char)),
    ('total_user_count', ctypes.c_int32),
    ('join_order', RcimOrder),
    ('user_info_vec', ctypes.POINTER(struct_RcimChatroomUserInfo)),
    ('user_info_vec_len', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

RcimChatroomInfo = struct_RcimChatroomInfo
RcimGetChatroomInfoCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimChatroomInfo))
RcimChatroomKvSyncLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char))
class struct_RcimChatroomKvInfo(Structure):
    pass

struct_RcimChatroomKvInfo._pack_ = 1 # source:False
struct_RcimChatroomKvInfo._fields_ = [
    ('key', ctypes.POINTER(ctypes.c_char)),
    ('value', ctypes.POINTER(ctypes.c_char)),
]

RcimChatroomKvInfo = struct_RcimChatroomKvInfo
RcimChatroomKvChangedLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimChatroomKvInfo), ctypes.c_int32)
RcimChatroomKvDeleteLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimChatroomKvInfo), ctypes.c_int32)
class struct_RcimChatroomKeyErrorInfo(Structure):
    pass

struct_RcimChatroomKeyErrorInfo._pack_ = 1 # source:False
struct_RcimChatroomKeyErrorInfo._fields_ = [
    ('key', ctypes.POINTER(ctypes.c_char)),
    ('error', RcimEngineError),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

RcimChatroomKeyErrorInfo = struct_RcimChatroomKeyErrorInfo
RcimChatroomKvCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimChatroomKeyErrorInfo), ctypes.c_int32)
RcimChatroomGetKvCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimChatroomKvInfo), ctypes.c_int32)
class struct_RcimLogInfo(Structure):
    pass

struct_RcimLogInfo._pack_ = 1 # source:False
struct_RcimLogInfo._fields_ = [
    ('session_id', ctypes.POINTER(ctypes.c_char)),
    ('log_type', RcimLogType),
    ('source', RcimLogSource),
    ('level', RcimLogLevel),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('tag', ctypes.POINTER(ctypes.c_char)),
    ('content', ctypes.POINTER(ctypes.c_char)),
    ('trace_id', ctypes.c_int64),
    ('create_time', ctypes.c_int64),
    ('location', ctypes.POINTER(ctypes.c_char)),
]

RcimLogInfo = struct_RcimLogInfo
RcimLogLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimLogInfo))
class struct_RcimInsertLogInfo(Structure):
    pass

struct_RcimInsertLogInfo._pack_ = 1 # source:False
struct_RcimInsertLogInfo._fields_ = [
    ('log_type', RcimLogType),
    ('source', RcimLogSource),
    ('level', RcimLogLevel),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('tag', ctypes.POINTER(ctypes.c_char)),
    ('content', ctypes.POINTER(ctypes.c_char)),
    ('trace_id', ctypes.c_int64),
    ('location', ctypes.POINTER(ctypes.c_char)),
]

RcimInsertLogInfo = struct_RcimInsertLogInfo
RcimDevLogLsr = ctypes.CFUNCTYPE(None, RcimDevLogLevel, ctypes.POINTER(ctypes.c_char))
class struct_RcimPublicServiceMenuItem(Structure):
    pass

struct_RcimPublicServiceMenuItem._pack_ = 1 # source:False
struct_RcimPublicServiceMenuItem._fields_ = [
    ('id', ctypes.POINTER(ctypes.c_char)),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('url', ctypes.POINTER(ctypes.c_char)),
    ('menu_type', RcimPublicServiceMenuItemType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('sub_menu_vec', ctypes.POINTER(struct_RcimPublicServiceMenuItem)),
    ('sub_menu_vec_len', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

RcimPublicServiceMenuItem = struct_RcimPublicServiceMenuItem
class struct_RcimPublicServiceInfo(Structure):
    pass

struct_RcimPublicServiceInfo._pack_ = 1 # source:False
struct_RcimPublicServiceInfo._fields_ = [
    ('target_id', ctypes.POINTER(ctypes.c_char)),
    ('conv_type', RcimConversationType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('portrait', ctypes.POINTER(ctypes.c_char)),
    ('introduction', ctypes.POINTER(ctypes.c_char)),
    ('is_followed', ctypes.c_bool),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('menu_vec', ctypes.POINTER(struct_RcimPublicServiceMenuItem)),
    ('menu_vec_len', ctypes.c_int32),
    ('is_global', ctypes.c_bool),
    ('PADDING_2', ctypes.c_ubyte * 3),
]

RcimPublicServiceInfo = struct_RcimPublicServiceInfo
RcimGetPublicServiceCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimPublicServiceInfo))
RcimGetLocalPublicServiceListCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(struct_RcimPublicServiceInfo), ctypes.c_int32)
class struct_RcimRtcConfig(Structure):
    pass

struct_RcimRtcConfig._pack_ = 1 # source:False
struct_RcimRtcConfig._fields_ = [
    ('log_server', ctypes.POINTER(ctypes.c_char)),
    ('data_center', ctypes.POINTER(ctypes.c_char)),
    ('jwt_token', ctypes.POINTER(ctypes.c_char)),
    ('open_gzip', ctypes.c_bool),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('voip_call_info', ctypes.POINTER(ctypes.c_char)),
]

RcimRtcConfig = struct_RcimRtcConfig
RcimVoipCallInfoLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimRtcConfig))
RcimSendRtcSignalingCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32)
RcimRtcHeartBeatSendLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char), ctypes.c_int64)
RcimRtcHeartBeatResultLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char), ctypes.c_int64, ctypes.c_int64)
RcimRtcRoomEventLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32)
RcimRtcSetKVSignalingCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), RcimEngineError, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
class struct_RcimRtcKvInfo(Structure):
    pass

struct_RcimRtcKvInfo._pack_ = 1 # source:False
struct_RcimRtcKvInfo._fields_ = [
    ('key', ctypes.POINTER(ctypes.c_char)),
    ('value', ctypes.POINTER(ctypes.c_char)),
]

RcimRtcKvInfo = struct_RcimRtcKvInfo
RcimRtcKvSignalingLsr = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_RcimRtcKvInfo), ctypes.c_int32)
RcimCmpSendCb = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_int32)
try:
    rcim_create_engine_builder = _libraries['FIXME_STUB'].rcim_create_engine_builder
    rcim_create_engine_builder.restype = RcimEngineError
    rcim_create_engine_builder.argtypes = [ctypes.POINTER(struct_RcimEngineBuilderParam), ctypes.POINTER(ctypes.POINTER(struct_RcimEngineBuilder))]
except AttributeError:
    pass
try:
    rcim_destroy_engine_builder = _libraries['FIXME_STUB'].rcim_destroy_engine_builder
    rcim_destroy_engine_builder.restype = RcimEngineError
    rcim_destroy_engine_builder.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder)]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_cloud_type = _libraries['FIXME_STUB'].rcim_engine_builder_set_cloud_type
    rcim_engine_builder_set_cloud_type.restype = RcimEngineError
    rcim_engine_builder_set_cloud_type.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), RcimCloudType]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_db_encrypted = _libraries['FIXME_STUB'].rcim_engine_builder_set_db_encrypted
    rcim_engine_builder_set_db_encrypted.restype = RcimEngineError
    rcim_engine_builder_set_db_encrypted.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.c_bool]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_enable_group_call = _libraries['FIXME_STUB'].rcim_engine_builder_set_enable_group_call
    rcim_engine_builder_set_enable_group_call.restype = RcimEngineError
    rcim_engine_builder_set_enable_group_call.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.c_bool]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_enable_reconnect_kick = _libraries['FIXME_STUB'].rcim_engine_builder_set_enable_reconnect_kick
    rcim_engine_builder_set_enable_reconnect_kick.restype = RcimEngineError
    rcim_engine_builder_set_enable_reconnect_kick.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.c_bool]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_store_path = _libraries['FIXME_STUB'].rcim_engine_builder_set_store_path
    rcim_engine_builder_set_store_path.restype = RcimEngineError
    rcim_engine_builder_set_store_path.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.POINTER(ctypes.c_char)]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_network_env = _libraries['FIXME_STUB'].rcim_engine_builder_set_network_env
    rcim_engine_builder_set_network_env.restype = RcimEngineError
    rcim_engine_builder_set_network_env.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.POINTER(ctypes.c_char)]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_file_path = _libraries['FIXME_STUB'].rcim_engine_builder_set_file_path
    rcim_engine_builder_set_file_path.restype = RcimEngineError
    rcim_engine_builder_set_file_path.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.POINTER(ctypes.c_char)]
except AttributeError:
    pass
int32_t = ctypes.c_int32
try:
    rcim_engine_builder_set_navi_server = _libraries['FIXME_STUB'].rcim_engine_builder_set_navi_server
    rcim_engine_builder_set_navi_server.restype = RcimEngineError
    rcim_engine_builder_set_navi_server.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_statistic_server = _libraries['FIXME_STUB'].rcim_engine_builder_set_statistic_server
    rcim_engine_builder_set_statistic_server.restype = RcimEngineError
    rcim_engine_builder_set_statistic_server.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.POINTER(ctypes.c_char)]
except AttributeError:
    pass
try:
    rcim_engine_builder_set_area_code = _libraries['FIXME_STUB'].rcim_engine_builder_set_area_code
    rcim_engine_builder_set_area_code.restype = RcimEngineError
    rcim_engine_builder_set_area_code.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), RcimAreaCode]
except AttributeError:
    pass
try:
    rcim_engine_builder_build = _libraries['FIXME_STUB'].rcim_engine_builder_build
    rcim_engine_builder_build.restype = RcimEngineError
    rcim_engine_builder_build.argtypes = [ctypes.POINTER(struct_RcimEngineBuilder), ctypes.POINTER(ctypes.POINTER(struct_RcimEngineSync))]
except AttributeError:
    pass
try:
    rcim_destroy_engine = _libraries['FIXME_STUB'].rcim_destroy_engine
    rcim_destroy_engine.restype = RcimEngineError
    rcim_destroy_engine.argtypes = [ctypes.POINTER(struct_RcimEngineSync)]
except AttributeError:
    pass
try:
    rcim_engine_set_database_status_listener = _libraries['FIXME_STUB'].rcim_engine_set_database_status_listener
    rcim_engine_set_database_status_listener.restype = RcimEngineError
    rcim_engine_set_database_status_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimDatabaseStatusLsr]
except AttributeError:
    pass
try:
    rcim_engine_get_sdk_version = _libraries['FIXME_STUB'].rcim_engine_get_sdk_version
    rcim_engine_get_sdk_version.restype = RcimEngineError
    rcim_engine_get_sdk_version.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
except AttributeError:
    pass
try:
    rcim_engine_set_device_id = _libraries['FIXME_STUB'].rcim_engine_set_device_id
    rcim_engine_set_device_id.restype = RcimEngineError
    rcim_engine_set_device_id.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char)]
except AttributeError:
    pass
try:
    rcim_engine_set_push_token = _libraries['FIXME_STUB'].rcim_engine_set_push_token
    rcim_engine_set_push_token.restype = RcimEngineError
    rcim_engine_set_push_token.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimPushTokenInfo), int32_t]
except AttributeError:
    pass
try:
    rcim_engine_get_delta_time = _libraries['FIXME_STUB'].rcim_engine_get_delta_time
    rcim_engine_get_delta_time.restype = RcimEngineError
    rcim_engine_get_delta_time.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_int64)]
except AttributeError:
    pass
try:
    rcim_engine_get_user_id = _libraries['FIXME_STUB'].rcim_engine_get_user_id
    rcim_engine_get_user_id.restype = RcimEngineError
    rcim_engine_get_user_id.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
except AttributeError:
    pass
try:
    rcim_engine_set_connection_status_listener = _libraries['FIXME_STUB'].rcim_engine_set_connection_status_listener
    rcim_engine_set_connection_status_listener.restype = RcimEngineError
    rcim_engine_set_connection_status_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimConnectionStatusLsr]
except AttributeError:
    pass
try:
    rcim_engine_get_connection_status = _libraries['FIXME_STUB'].rcim_engine_get_connection_status
    rcim_engine_get_connection_status.restype = RcimEngineError
    rcim_engine_get_connection_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConnectionStatus)]
except AttributeError:
    pass
try:
    rcim_engine_connect = _libraries['FIXME_STUB'].rcim_engine_connect
    rcim_engine_connect.restype = None
    rcim_engine_connect.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), int32_t, ctypes.POINTER(None), RcimConnectCb]
except AttributeError:
    pass
try:
    rcim_engine_disconnect = _libraries['FIXME_STUB'].rcim_engine_disconnect
    rcim_engine_disconnect.restype = None
    rcim_engine_disconnect.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimDisconnectMode, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_notify_app_state_changed = _libraries['FIXME_STUB'].rcim_engine_notify_app_state_changed
    rcim_engine_notify_app_state_changed.restype = RcimEngineError
    rcim_engine_notify_app_state_changed.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimAppState]
except AttributeError:
    pass
try:
    rcim_engine_notify_network_changed = _libraries['FIXME_STUB'].rcim_engine_notify_network_changed
    rcim_engine_notify_network_changed.restype = RcimEngineError
    rcim_engine_notify_network_changed.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimNetworkType]
except AttributeError:
    pass
try:
    rcim_engine_set_message_received_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_received_listener
    rcim_engine_set_message_received_listener.restype = RcimEngineError
    rcim_engine_set_message_received_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageReceivedLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_offline_message_sync_completed_listener = _libraries['FIXME_STUB'].rcim_engine_set_offline_message_sync_completed_listener
    rcim_engine_set_offline_message_sync_completed_listener.restype = RcimEngineError
    rcim_engine_set_offline_message_sync_completed_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimOfflineMessageSyncCompletedLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_message_searchable_words_callback_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_searchable_words_callback_listener
    rcim_engine_set_message_searchable_words_callback_listener.restype = RcimEngineError
    rcim_engine_set_message_searchable_words_callback_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageSearchableWordsCbLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_sight_compress_callback_listener = _libraries['FIXME_STUB'].rcim_engine_set_sight_compress_callback_listener
    rcim_engine_set_sight_compress_callback_listener.restype = RcimEngineError
    rcim_engine_set_sight_compress_callback_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimSightCompressCbLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_message_recalled_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_recalled_listener
    rcim_engine_set_message_recalled_listener.restype = RcimEngineError
    rcim_engine_set_message_recalled_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimRecallMessageLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_message_blocked_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_blocked_listener
    rcim_engine_set_message_blocked_listener.restype = RcimEngineError
    rcim_engine_set_message_blocked_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageBlockedLsr]
except AttributeError:
    pass
try:
    rcim_engine_send_message = _libraries['FIXME_STUB'].rcim_engine_send_message
    rcim_engine_send_message.restype = None
    rcim_engine_send_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(struct_RcimSendMessageOption), ctypes.POINTER(None), RcimCodeMessageCb, RcimMessageCb]
except AttributeError:
    pass
int64_t = ctypes.c_int64
try:
    rcim_engine_send_read_receipt_message = _libraries['FIXME_STUB'].rcim_engine_send_read_receipt_message
    rcim_engine_send_read_receipt_message.restype = None
    rcim_engine_send_read_receipt_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, ctypes.POINTER(None), RcimCodeMessageCb]
except AttributeError:
    pass
try:
    rcim_engine_send_read_receipt_request = _libraries['FIXME_STUB'].rcim_engine_send_read_receipt_request
    rcim_engine_send_read_receipt_request.restype = None
    rcim_engine_send_read_receipt_request.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_send_read_receipt_response = _libraries['FIXME_STUB'].rcim_engine_send_read_receipt_response
    rcim_engine_send_read_receipt_response.restype = None
    rcim_engine_send_read_receipt_response.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimSendReadReceiptResponseMessageData), int32_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_set_read_receipt_received_listener = _libraries['FIXME_STUB'].rcim_engine_set_read_receipt_received_listener
    rcim_engine_set_read_receipt_received_listener.restype = RcimEngineError
    rcim_engine_set_read_receipt_received_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageNotifyLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_read_receipt_request_listener = _libraries['FIXME_STUB'].rcim_engine_set_read_receipt_request_listener
    rcim_engine_set_read_receipt_request_listener.restype = RcimEngineError
    rcim_engine_set_read_receipt_request_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimReadReceiptRequestLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_read_receipt_response_listener = _libraries['FIXME_STUB'].rcim_engine_set_read_receipt_response_listener
    rcim_engine_set_read_receipt_response_listener.restype = RcimEngineError
    rcim_engine_set_read_receipt_response_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimReadReceiptResponseLsr]
except AttributeError:
    pass
try:
    rcim_engine_send_read_receipt_response_v2 = _libraries['FIXME_STUB'].rcim_engine_send_read_receipt_response_v2
    rcim_engine_send_read_receipt_response_v2.restype = None
    rcim_engine_send_read_receipt_response_v2.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_read_receipt_v2_readers = _libraries['FIXME_STUB'].rcim_engine_get_read_receipt_v2_readers
    rcim_engine_get_read_receipt_v2_readers.restype = None
    rcim_engine_get_read_receipt_v2_readers.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetReadReceiptV2ReaderListCb]
except AttributeError:
    pass
try:
    rcim_engine_set_read_receipt_response_v2_listener = _libraries['FIXME_STUB'].rcim_engine_set_read_receipt_response_v2_listener
    rcim_engine_set_read_receipt_response_v2_listener.restype = RcimEngineError
    rcim_engine_set_read_receipt_response_v2_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimReadReceiptResponseV2Lsr]
except AttributeError:
    pass
try:
    rcim_engine_cancel_send_media_message = _libraries['FIXME_STUB'].rcim_engine_cancel_send_media_message
    rcim_engine_cancel_send_media_message.restype = None
    rcim_engine_cancel_send_media_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_send_media_message = _libraries['FIXME_STUB'].rcim_engine_send_media_message
    rcim_engine_send_media_message.restype = None
    rcim_engine_send_media_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(struct_RcimSendMessageOption), ctypes.POINTER(None), RcimCodeMessageCb, RcimMessageCb, RcimSendMessageOnProgressCb, RcimMediaMessageHandlerCb]
except AttributeError:
    pass
try:
    rcim_engine_download_media_message = _libraries['FIXME_STUB'].rcim_engine_download_media_message
    rcim_engine_download_media_message.restype = None
    rcim_engine_download_media_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(None), RcimDownloadMediaCb, RcimDownloadMessageProgressCb, RcimMediaMessageHandlerCb]
except AttributeError:
    pass
try:
    rcim_engine_cancel_download_media_message = _libraries['FIXME_STUB'].rcim_engine_cancel_download_media_message
    rcim_engine_cancel_download_media_message.restype = None
    rcim_engine_cancel_download_media_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_pause_download_media_message = _libraries['FIXME_STUB'].rcim_engine_pause_download_media_message
    rcim_engine_pause_download_media_message.restype = None
    rcim_engine_pause_download_media_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_download_file_with_progress = _libraries['FIXME_STUB'].rcim_engine_download_file_with_progress
    rcim_engine_download_file_with_progress.restype = None
    rcim_engine_download_file_with_progress.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(None), RcimDownloadMediaCb, RcimDownloadFileProgressCb]
except AttributeError:
    pass
try:
    rcim_engine_download_file_with_unique_id = _libraries['FIXME_STUB'].rcim_engine_download_file_with_unique_id
    rcim_engine_download_file_with_unique_id.restype = None
    rcim_engine_download_file_with_unique_id.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimDownloadMediaCb, RcimDownloadFileProgressCb]
except AttributeError:
    pass
try:
    rcim_engine_cancel_download_file = _libraries['FIXME_STUB'].rcim_engine_cancel_download_file
    rcim_engine_cancel_download_file.restype = None
    rcim_engine_cancel_download_file.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_pause_download_file = _libraries['FIXME_STUB'].rcim_engine_pause_download_file
    rcim_engine_pause_download_file.restype = None
    rcim_engine_pause_download_file.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_recall_message = _libraries['FIXME_STUB'].rcim_engine_recall_message
    rcim_engine_recall_message.restype = None
    rcim_engine_recall_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(None), RcimRecallMessageCb]
except AttributeError:
    pass
try:
    rcim_engine_register_message_types = _libraries['FIXME_STUB'].rcim_engine_register_message_types
    rcim_engine_register_message_types.restype = RcimEngineError
    rcim_engine_register_message_types.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageType), int32_t]
except AttributeError:
    pass
try:
    rcim_engine_get_local_message_by_uid = _libraries['FIXME_STUB'].rcim_engine_get_local_message_by_uid
    rcim_engine_get_local_message_by_uid.restype = None
    rcim_engine_get_local_message_by_uid.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimCodeMessageCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_message_by_id = _libraries['FIXME_STUB'].rcim_engine_get_local_message_by_id
    rcim_engine_get_local_message_by_id.restype = None
    rcim_engine_get_local_message_by_id.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(None), RcimCodeMessageCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_history_messages_by_time = _libraries['FIXME_STUB'].rcim_engine_get_local_history_messages_by_time
    rcim_engine_get_local_history_messages_by_time.restype = None
    rcim_engine_get_local_history_messages_by_time.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, int64_t, int32_t, int32_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_history_messages_by_senders = _libraries['FIXME_STUB'].rcim_engine_get_local_history_messages_by_senders
    rcim_engine_get_local_history_messages_by_senders.restype = None
    rcim_engine_get_local_history_messages_by_senders.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, int32_t, int64_t, RcimOrder, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_history_messages_by_id = _libraries['FIXME_STUB'].rcim_engine_get_local_history_messages_by_id
    rcim_engine_get_local_history_messages_by_id.restype = None
    rcim_engine_get_local_history_messages_by_id.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, int64_t, int32_t, int32_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_remote_history_messages = _libraries['FIXME_STUB'].rcim_engine_get_remote_history_messages
    rcim_engine_get_remote_history_messages.restype = None
    rcim_engine_get_remote_history_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, int32_t, RcimOrder, ctypes.c_bool, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_clean_local_history_messages = _libraries['FIXME_STUB'].rcim_engine_clean_local_history_messages
    rcim_engine_clean_local_history_messages.restype = None
    rcim_engine_clean_local_history_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_clean_remote_history_messages = _libraries['FIXME_STUB'].rcim_engine_clean_remote_history_messages
    rcim_engine_clean_remote_history_messages.restype = None
    rcim_engine_clean_remote_history_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_insert_local_messages = _libraries['FIXME_STUB'].rcim_engine_insert_local_messages
    rcim_engine_insert_local_messages.restype = None
    rcim_engine_insert_local_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), int32_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_insert_local_message = _libraries['FIXME_STUB'].rcim_engine_insert_local_message
    rcim_engine_insert_local_message.restype = None
    rcim_engine_insert_local_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(None), RcimCodeMessageCb]
except AttributeError:
    pass
try:
    rcim_engine_delete_local_messages = _libraries['FIXME_STUB'].rcim_engine_delete_local_messages
    rcim_engine_delete_local_messages.restype = None
    rcim_engine_delete_local_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_delete_local_messages_by_ids = _libraries['FIXME_STUB'].rcim_engine_delete_local_messages_by_ids
    rcim_engine_delete_local_messages_by_ids.restype = None
    rcim_engine_delete_local_messages_by_ids.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_int64), int32_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_delete_remote_messages = _libraries['FIXME_STUB'].rcim_engine_delete_remote_messages
    rcim_engine_delete_remote_messages.restype = None
    rcim_engine_delete_remote_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimMessageBox), int32_t, ctypes.c_bool, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_search_local_messages = _libraries['FIXME_STUB'].rcim_engine_search_local_messages
    rcim_engine_search_local_messages.restype = None
    rcim_engine_search_local_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int32_t, int64_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_search_local_messages_by_object_name = _libraries['FIXME_STUB'].rcim_engine_search_local_messages_by_object_name
    rcim_engine_search_local_messages_by_object_name.restype = None
    rcim_engine_search_local_messages_by_object_name.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, int32_t, int64_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_search_local_messages_by_time = _libraries['FIXME_STUB'].rcim_engine_search_local_messages_by_time
    rcim_engine_search_local_messages_by_time.restype = None
    rcim_engine_search_local_messages_by_time.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int32_t, int64_t, int64_t, int64_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_search_local_messages_by_user_id = _libraries['FIXME_STUB'].rcim_engine_search_local_messages_by_user_id
    rcim_engine_search_local_messages_by_user_id.restype = None
    rcim_engine_search_local_messages_by_user_id.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int32_t, int64_t, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_search_local_messages_by_multiple_conversations = _libraries['FIXME_STUB'].rcim_engine_search_local_messages_by_multiple_conversations
    rcim_engine_search_local_messages_by_multiple_conversations.restype = None
    rcim_engine_search_local_messages_by_multiple_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(ctypes.c_char), int32_t, int64_t, RcimOrder, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_set_message_expansion_update_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_expansion_update_listener
    rcim_engine_set_message_expansion_update_listener.restype = RcimEngineError
    rcim_engine_set_message_expansion_update_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageExpansionKvUpdateLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_message_expansion_remove_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_expansion_remove_listener
    rcim_engine_set_message_expansion_remove_listener.restype = RcimEngineError
    rcim_engine_set_message_expansion_remove_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageExpansionKvRemoveLsr]
except AttributeError:
    pass
try:
    rcim_engine_update_message_expansion = _libraries['FIXME_STUB'].rcim_engine_update_message_expansion
    rcim_engine_update_message_expansion.restype = None
    rcim_engine_update_message_expansion.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageExpansionKvInfo), int32_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_remove_message_expansion = _libraries['FIXME_STUB'].rcim_engine_remove_message_expansion
    rcim_engine_remove_message_expansion.restype = None
    rcim_engine_remove_message_expansion.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_message_sent_status = _libraries['FIXME_STUB'].rcim_engine_set_message_sent_status
    rcim_engine_set_message_sent_status.restype = None
    rcim_engine_set_message_sent_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, RcimSentStatus, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_message_received_status = _libraries['FIXME_STUB'].rcim_engine_set_message_received_status
    rcim_engine_set_message_received_status.restype = None
    rcim_engine_set_message_received_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(struct_RcimReceivedStatus), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_message_content = _libraries['FIXME_STUB'].rcim_engine_set_message_content
    rcim_engine_set_message_content.restype = None
    rcim_engine_set_message_content.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_message_extra = _libraries['FIXME_STUB'].rcim_engine_set_message_extra
    rcim_engine_set_message_extra.restype = None
    rcim_engine_set_message_extra.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int64_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_push_content_show_status = _libraries['FIXME_STUB'].rcim_engine_set_push_content_show_status
    rcim_engine_set_push_content_show_status.restype = None
    rcim_engine_set_push_content_show_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.c_bool, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_push_content_show_status = _libraries['FIXME_STUB'].rcim_engine_get_push_content_show_status
    rcim_engine_get_push_content_show_status.restype = None
    rcim_engine_get_push_content_show_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimGetBoolCb]
except AttributeError:
    pass
try:
    rcim_engine_set_push_receive_status = _libraries['FIXME_STUB'].rcim_engine_set_push_receive_status
    rcim_engine_set_push_receive_status.restype = None
    rcim_engine_set_push_receive_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.c_bool, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_push_receive_status = _libraries['FIXME_STUB'].rcim_engine_get_push_receive_status
    rcim_engine_get_push_receive_status.restype = None
    rcim_engine_get_push_receive_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimGetBoolCb]
except AttributeError:
    pass
try:
    rcim_engine_set_message_destructing_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_destructing_listener
    rcim_engine_set_message_destructing_listener.restype = RcimEngineError
    rcim_engine_set_message_destructing_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageDestructingLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_message_destruction_stop_listener = _libraries['FIXME_STUB'].rcim_engine_set_message_destruction_stop_listener
    rcim_engine_set_message_destruction_stop_listener.restype = RcimEngineError
    rcim_engine_set_message_destruction_stop_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimMessageDestructionStopLsr]
except AttributeError:
    pass
try:
    rcim_engine_message_begin_destruct = _libraries['FIXME_STUB'].rcim_engine_message_begin_destruct
    rcim_engine_message_begin_destruct.restype = None
    rcim_engine_message_begin_destruct.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_message_stop_destruct = _libraries['FIXME_STUB'].rcim_engine_message_stop_destruct
    rcim_engine_message_stop_destruct.restype = None
    rcim_engine_message_stop_destruct.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimMessageBox), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_conversation_status_listener = _libraries['FIXME_STUB'].rcim_engine_set_conversation_status_listener
    rcim_engine_set_conversation_status_listener.restype = RcimEngineError
    rcim_engine_set_conversation_status_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimConversationStatusLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_typing_status_listener = _libraries['FIXME_STUB'].rcim_engine_set_typing_status_listener
    rcim_engine_set_typing_status_listener.restype = RcimEngineError
    rcim_engine_set_typing_status_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimTypingStatusLsr]
except AttributeError:
    pass
try:
    rcim_engine_send_typing_status = _libraries['FIXME_STUB'].rcim_engine_send_typing_status
    rcim_engine_send_typing_status.restype = None
    rcim_engine_send_typing_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_typing_status_interval = _libraries['FIXME_STUB'].rcim_engine_set_typing_status_interval
    rcim_engine_set_typing_status_interval.restype = None
    rcim_engine_set_typing_status_interval.argtypes = [ctypes.POINTER(struct_RcimEngineSync), int32_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_conversation = _libraries['FIXME_STUB'].rcim_engine_get_local_conversation
    rcim_engine_get_local_conversation.restype = None
    rcim_engine_get_local_conversation.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetConversationCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_conversations_by_page = _libraries['FIXME_STUB'].rcim_engine_get_local_conversations_by_page
    rcim_engine_get_local_conversations_by_page.restype = None
    rcim_engine_get_local_conversations_by_page.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, int64_t, int32_t, ctypes.POINTER(None), RcimGetConversationListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_pin_conversations_by_page = _libraries['FIXME_STUB'].rcim_engine_get_local_pin_conversations_by_page
    rcim_engine_get_local_pin_conversations_by_page.restype = None
    rcim_engine_get_local_pin_conversations_by_page.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, int64_t, int32_t, ctypes.c_bool, ctypes.POINTER(None), RcimGetConversationListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_muted_conversations_by_page = _libraries['FIXME_STUB'].rcim_engine_get_local_muted_conversations_by_page
    rcim_engine_get_local_muted_conversations_by_page.restype = None
    rcim_engine_get_local_muted_conversations_by_page.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, int64_t, int32_t, ctypes.POINTER(RcimPushNotificationMuteLevel), int32_t, ctypes.POINTER(None), RcimGetConversationListCb]
except AttributeError:
    pass
try:
    rcim_engine_clear_local_conversations = _libraries['FIXME_STUB'].rcim_engine_clear_local_conversations
    rcim_engine_clear_local_conversations.restype = None
    rcim_engine_clear_local_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_remove_conversations = _libraries['FIXME_STUB'].rcim_engine_remove_conversations
    rcim_engine_remove_conversations.restype = None
    rcim_engine_remove_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimConversationIdentifier), int32_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_pin_conversations = _libraries['FIXME_STUB'].rcim_engine_pin_conversations
    rcim_engine_pin_conversations.restype = None
    rcim_engine_pin_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimConversationIdentifier), int32_t, ctypes.c_bool, ctypes.c_bool, ctypes.c_bool, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_conversation_pin_status = _libraries['FIXME_STUB'].rcim_engine_get_local_conversation_pin_status
    rcim_engine_get_local_conversation_pin_status.restype = None
    rcim_engine_get_local_conversation_pin_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetBoolCb]
except AttributeError:
    pass
try:
    rcim_engine_mute_conversations = _libraries['FIXME_STUB'].rcim_engine_mute_conversations
    rcim_engine_mute_conversations.restype = None
    rcim_engine_mute_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimConversationIdentifier), int32_t, RcimPushNotificationMuteLevel, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_conversation_mute_level = _libraries['FIXME_STUB'].rcim_engine_get_local_conversation_mute_level
    rcim_engine_get_local_conversation_mute_level.restype = None
    rcim_engine_get_local_conversation_mute_level.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetLocalConversationMuteLevelCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_unread_conversation = _libraries['FIXME_STUB'].rcim_engine_get_local_unread_conversation
    rcim_engine_get_local_unread_conversation.restype = None
    rcim_engine_get_local_unread_conversation.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, ctypes.POINTER(None), RcimGetConversationListCb]
except AttributeError:
    pass
try:
    rcim_engine_search_local_conversations = _libraries['FIXME_STUB'].rcim_engine_search_local_conversations
    rcim_engine_search_local_conversations.restype = None
    rcim_engine_search_local_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetConversationListCb]
except AttributeError:
    pass
try:
    rcim_engine_set_no_disturbing = _libraries['FIXME_STUB'].rcim_engine_set_no_disturbing
    rcim_engine_set_no_disturbing.restype = None
    rcim_engine_set_no_disturbing.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), int32_t, RcimPushNotificationMuteLevel, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_unset_no_disturbing = _libraries['FIXME_STUB'].rcim_engine_unset_no_disturbing
    rcim_engine_unset_no_disturbing.restype = None
    rcim_engine_unset_no_disturbing.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_no_disturbing = _libraries['FIXME_STUB'].rcim_engine_get_no_disturbing
    rcim_engine_get_no_disturbing.restype = None
    rcim_engine_get_no_disturbing.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimGetNoDisturbingCb]
except AttributeError:
    pass
try:
    rcim_engine_save_text_message_draft = _libraries['FIXME_STUB'].rcim_engine_save_text_message_draft
    rcim_engine_save_text_message_draft.restype = None
    rcim_engine_save_text_message_draft.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_text_message_draft = _libraries['FIXME_STUB'].rcim_engine_get_text_message_draft
    rcim_engine_get_text_message_draft.restype = None
    rcim_engine_get_text_message_draft.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetTextMessageDraftCb]
except AttributeError:
    pass
try:
    rcim_engine_get_total_unread_count = _libraries['FIXME_STUB'].rcim_engine_get_total_unread_count
    rcim_engine_get_total_unread_count.restype = None
    rcim_engine_get_total_unread_count.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimGetCountCb]
except AttributeError:
    pass
try:
    rcim_engine_get_unread_count_by_conversations = _libraries['FIXME_STUB'].rcim_engine_get_unread_count_by_conversations
    rcim_engine_get_unread_count_by_conversations.restype = None
    rcim_engine_get_unread_count_by_conversations.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimConversationIdentifier), int32_t, ctypes.POINTER(None), RcimGetCountCb]
except AttributeError:
    pass
try:
    rcim_engine_get_unread_count = _libraries['FIXME_STUB'].rcim_engine_get_unread_count
    rcim_engine_get_unread_count.restype = None
    rcim_engine_get_unread_count.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetCountCb]
except AttributeError:
    pass
try:
    rcim_engine_get_unread_count_by_conversation_types = _libraries['FIXME_STUB'].rcim_engine_get_unread_count_by_conversation_types
    rcim_engine_get_unread_count_by_conversation_types.restype = None
    rcim_engine_get_unread_count_by_conversation_types.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(RcimConversationType), int32_t, ctypes.c_bool, ctypes.POINTER(None), RcimGetCountCb]
except AttributeError:
    pass
try:
    rcim_engine_clear_messages_unread_status = _libraries['FIXME_STUB'].rcim_engine_clear_messages_unread_status
    rcim_engine_clear_messages_unread_status.restype = None
    rcim_engine_clear_messages_unread_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_clear_messages_unread_status_by_send_time = _libraries['FIXME_STUB'].rcim_engine_clear_messages_unread_status_by_send_time
    rcim_engine_clear_messages_unread_status_by_send_time.restype = None
    rcim_engine_clear_messages_unread_status_by_send_time.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_sync_conversation_read_status = _libraries['FIXME_STUB'].rcim_engine_sync_conversation_read_status
    rcim_engine_sync_conversation_read_status.restype = None
    rcim_engine_sync_conversation_read_status.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int64_t, ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_set_sync_conversation_read_status_listener = _libraries['FIXME_STUB'].rcim_engine_set_sync_conversation_read_status_listener
    rcim_engine_set_sync_conversation_read_status_listener.restype = RcimEngineError
    rcim_engine_set_sync_conversation_read_status_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimConversationReadStatusLsr]
except AttributeError:
    pass
try:
    rcim_engine_get_unread_mentioned_messages = _libraries['FIXME_STUB'].rcim_engine_get_unread_mentioned_messages
    rcim_engine_get_unread_mentioned_messages.restype = None
    rcim_engine_get_unread_mentioned_messages.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), int32_t, RcimOrder, ctypes.POINTER(None), RcimGetMessageListCb]
except AttributeError:
    pass
try:
    rcim_engine_get_first_unread_message = _libraries['FIXME_STUB'].rcim_engine_get_first_unread_message
    rcim_engine_get_first_unread_message.restype = None
    rcim_engine_get_first_unread_message.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimConversationType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimCodeMessageCb]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_status_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_status_listener
    rcim_engine_set_chatroom_status_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_status_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomStatusLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_member_changed_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_member_changed_listener
    rcim_engine_set_chatroom_member_changed_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_member_changed_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomMemberChangedLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_member_banned_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_member_banned_listener
    rcim_engine_set_chatroom_member_banned_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_member_banned_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomMemberBannedLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_member_blocked_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_member_blocked_listener
    rcim_engine_set_chatroom_member_blocked_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_member_blocked_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomMemberBlockedLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_multi_client_sync_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_multi_client_sync_listener
    rcim_engine_set_chatroom_multi_client_sync_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_multi_client_sync_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomMultiClientSyncLsr]
except AttributeError:
    pass
try:
    rcim_engine_join_chatroom = _libraries['FIXME_STUB'].rcim_engine_join_chatroom
    rcim_engine_join_chatroom.restype = None
    rcim_engine_join_chatroom.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), int32_t, ctypes.POINTER(None), RcimJoinChatroomCb]
except AttributeError:
    pass
try:
    rcim_engine_join_existing_chatroom = _libraries['FIXME_STUB'].rcim_engine_join_existing_chatroom
    rcim_engine_join_existing_chatroom.restype = None
    rcim_engine_join_existing_chatroom.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), int32_t, ctypes.POINTER(None), RcimJoinExistingChatroomCb]
except AttributeError:
    pass
try:
    rcim_engine_quit_chatroom = _libraries['FIXME_STUB'].rcim_engine_quit_chatroom
    rcim_engine_quit_chatroom.restype = None
    rcim_engine_quit_chatroom.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimEngineErrorCb]
except AttributeError:
    pass
try:
    rcim_engine_get_chatroom_info = _libraries['FIXME_STUB'].rcim_engine_get_chatroom_info
    rcim_engine_get_chatroom_info.restype = None
    rcim_engine_get_chatroom_info.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), int32_t, RcimOrder, ctypes.POINTER(None), RcimGetChatroomInfoCb]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_kv_sync_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_kv_sync_listener
    rcim_engine_set_chatroom_kv_sync_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_kv_sync_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomKvSyncLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_kv_changed_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_kv_changed_listener
    rcim_engine_set_chatroom_kv_changed_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_kv_changed_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomKvChangedLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_kv_delete_listener = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_kv_delete_listener
    rcim_engine_set_chatroom_kv_delete_listener.restype = RcimEngineError
    rcim_engine_set_chatroom_kv_delete_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimChatroomKvDeleteLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_chatroom_kvs = _libraries['FIXME_STUB'].rcim_engine_set_chatroom_kvs
    rcim_engine_set_chatroom_kvs.restype = None
    rcim_engine_set_chatroom_kvs.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(struct_RcimChatroomKvInfo), int32_t, ctypes.c_bool, ctypes.c_bool, ctypes.POINTER(None), RcimChatroomKvCb]
except AttributeError:
    pass
try:
    rcim_engine_delete_chatroom_kvs = _libraries['FIXME_STUB'].rcim_engine_delete_chatroom_kvs
    rcim_engine_delete_chatroom_kvs.restype = None
    rcim_engine_delete_chatroom_kvs.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.c_bool, ctypes.POINTER(None), RcimChatroomKvCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_chatroom_kv_by_keys = _libraries['FIXME_STUB'].rcim_engine_get_local_chatroom_kv_by_keys
    rcim_engine_get_local_chatroom_kv_by_keys.restype = None
    rcim_engine_get_local_chatroom_kv_by_keys.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, ctypes.POINTER(None), RcimChatroomGetKvCb]
except AttributeError:
    pass
try:
    rcim_engine_get_chatroom_all_kvs = _libraries['FIXME_STUB'].rcim_engine_get_chatroom_all_kvs
    rcim_engine_get_chatroom_all_kvs.restype = None
    rcim_engine_get_chatroom_all_kvs.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimChatroomGetKvCb]
except AttributeError:
    pass
try:
    rcim_engine_set_log_listener = _libraries['FIXME_STUB'].rcim_engine_set_log_listener
    rcim_engine_set_log_listener.restype = RcimEngineError
    rcim_engine_set_log_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimLogLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_log_filter = _libraries['FIXME_STUB'].rcim_engine_set_log_filter
    rcim_engine_set_log_filter.restype = RcimEngineError
    rcim_engine_set_log_filter.argtypes = [ctypes.POINTER(struct_RcimEngineSync), RcimLogLevel]
except AttributeError:
    pass
try:
    rcim_engine_insert_log = _libraries['FIXME_STUB'].rcim_engine_insert_log
    rcim_engine_insert_log.restype = RcimEngineError
    rcim_engine_insert_log.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(struct_RcimInsertLogInfo)]
except AttributeError:
    pass
try:
    rcim_dev_log_init = _libraries['FIXME_STUB'].rcim_dev_log_init
    rcim_dev_log_init.restype = None
    rcim_dev_log_init.argtypes = [RcimDevLogLsr]
except AttributeError:
    pass
try:
    rcim_engine_get_local_public_service = _libraries['FIXME_STUB'].rcim_engine_get_local_public_service
    rcim_engine_get_local_public_service.restype = None
    rcim_engine_get_local_public_service.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimGetPublicServiceCb]
except AttributeError:
    pass
try:
    rcim_engine_get_local_all_public_services = _libraries['FIXME_STUB'].rcim_engine_get_local_all_public_services
    rcim_engine_get_local_all_public_services.restype = None
    rcim_engine_get_local_all_public_services.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimGetLocalPublicServiceListCb]
except AttributeError:
    pass
try:
    rcim_engine_set_voip_call_info_listener = _libraries['FIXME_STUB'].rcim_engine_set_voip_call_info_listener
    rcim_engine_set_voip_call_info_listener.restype = RcimEngineError
    rcim_engine_set_voip_call_info_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimVoipCallInfoLsr]
except AttributeError:
    pass
try:
    rcim_engine_send_rtc_signaling = _libraries['FIXME_STUB'].rcim_engine_send_rtc_signaling
    rcim_engine_send_rtc_signaling.restype = None
    rcim_engine_send_rtc_signaling.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_bool, ctypes.POINTER(ctypes.c_ubyte), int32_t, int32_t, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(None), RcimSendRtcSignalingCb]
except AttributeError:
    pass
try:
    rcim_engine_cancel_rtc_signaling = _libraries['FIXME_STUB'].rcim_engine_cancel_rtc_signaling
    rcim_engine_cancel_rtc_signaling.restype = RcimEngineError
    rcim_engine_cancel_rtc_signaling.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_int64), int32_t]
except AttributeError:
    pass
try:
    rcim_engine_set_rtc_heartbeat_send_listener = _libraries['FIXME_STUB'].rcim_engine_set_rtc_heartbeat_send_listener
    rcim_engine_set_rtc_heartbeat_send_listener.restype = RcimEngineError
    rcim_engine_set_rtc_heartbeat_send_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimRtcHeartBeatSendLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_rtc_heartbeat_send_result_listener = _libraries['FIXME_STUB'].rcim_engine_set_rtc_heartbeat_send_result_listener
    rcim_engine_set_rtc_heartbeat_send_result_listener.restype = RcimEngineError
    rcim_engine_set_rtc_heartbeat_send_result_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimRtcHeartBeatResultLsr]
except AttributeError:
    pass
try:
    rcim_engine_set_rtc_room_event_listener = _libraries['FIXME_STUB'].rcim_engine_set_rtc_room_event_listener
    rcim_engine_set_rtc_room_event_listener.restype = RcimEngineError
    rcim_engine_set_rtc_room_event_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimRtcRoomEventLsr]
except AttributeError:
    pass
try:
    rcim_engine_send_rtc_heartbeat = _libraries['FIXME_STUB'].rcim_engine_send_rtc_heartbeat
    rcim_engine_send_rtc_heartbeat.restype = RcimEngineError
    rcim_engine_send_rtc_heartbeat.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), int32_t, int32_t]
except AttributeError:
    pass
try:
    rcim_engine_rtc_set_kv_signaling = _libraries['FIXME_STUB'].rcim_engine_rtc_set_kv_signaling
    rcim_engine_rtc_set_kv_signaling.restype = None
    rcim_engine_rtc_set_kv_signaling.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), RcimRtcSetKVSignalingCb]
except AttributeError:
    pass
try:
    rcim_engine_set_rtc_kv_signaling_listener = _libraries['FIXME_STUB'].rcim_engine_set_rtc_kv_signaling_listener
    rcim_engine_set_rtc_kv_signaling_listener.restype = RcimEngineError
    rcim_engine_set_rtc_kv_signaling_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimRtcKvSignalingLsr]
except AttributeError:
    pass
try:
    rcim_malloc_message_box = _libraries['FIXME_STUB'].rcim_malloc_message_box
    rcim_malloc_message_box.restype = ctypes.POINTER(struct_RcimMessageBox)
    rcim_malloc_message_box.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_message_box = _libraries['FIXME_STUB'].rcim_free_message_box
    rcim_free_message_box.restype = None
    rcim_free_message_box.argtypes = [ctypes.POINTER(struct_RcimMessageBox)]
except AttributeError:
    pass
try:
    rcim_malloc_message_box_vec = _libraries['FIXME_STUB'].rcim_malloc_message_box_vec
    rcim_malloc_message_box_vec.restype = ctypes.POINTER(struct_RcimMessageBox)
    rcim_malloc_message_box_vec.argtypes = [int32_t]
except AttributeError:
    pass
try:
    rcim_free_message_box_vec = _libraries['FIXME_STUB'].rcim_free_message_box_vec
    rcim_free_message_box_vec.restype = None
    rcim_free_message_box_vec.argtypes = [ctypes.POINTER(struct_RcimMessageBox), int32_t]
except AttributeError:
    pass
try:
    rcim_malloc_receive_status = _libraries['FIXME_STUB'].rcim_malloc_receive_status
    rcim_malloc_receive_status.restype = ctypes.POINTER(struct_RcimReceivedStatus)
    rcim_malloc_receive_status.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_receive_status = _libraries['FIXME_STUB'].rcim_free_receive_status
    rcim_free_receive_status.restype = None
    rcim_free_receive_status.argtypes = [ctypes.POINTER(struct_RcimReceivedStatus)]
except AttributeError:
    pass
try:
    rcim_malloc_push_config = _libraries['FIXME_STUB'].rcim_malloc_push_config
    rcim_malloc_push_config.restype = ctypes.POINTER(struct_RcimPushConfig)
    rcim_malloc_push_config.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_push_config = _libraries['FIXME_STUB'].rcim_free_push_config
    rcim_free_push_config.restype = None
    rcim_free_push_config.argtypes = [ctypes.POINTER(struct_RcimPushConfig)]
except AttributeError:
    pass
try:
    rcim_malloc_ios_config = _libraries['FIXME_STUB'].rcim_malloc_ios_config
    rcim_malloc_ios_config.restype = ctypes.POINTER(struct_RcimIosConfig)
    rcim_malloc_ios_config.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_ios_config = _libraries['FIXME_STUB'].rcim_free_ios_config
    rcim_free_ios_config.restype = None
    rcim_free_ios_config.argtypes = [ctypes.POINTER(struct_RcimIosConfig)]
except AttributeError:
    pass
try:
    rcim_malloc_android_config = _libraries['FIXME_STUB'].rcim_malloc_android_config
    rcim_malloc_android_config.restype = ctypes.POINTER(struct_RcimAndroidConfig)
    rcim_malloc_android_config.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_android_config = _libraries['FIXME_STUB'].rcim_free_android_config
    rcim_free_android_config.restype = None
    rcim_free_android_config.argtypes = [ctypes.POINTER(struct_RcimAndroidConfig)]
except AttributeError:
    pass
try:
    rcim_malloc_harmony_config = _libraries['FIXME_STUB'].rcim_malloc_harmony_config
    rcim_malloc_harmony_config.restype = ctypes.POINTER(struct_RcimHarmonyConfig)
    rcim_malloc_harmony_config.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_harmony_config = _libraries['FIXME_STUB'].rcim_free_harmony_config
    rcim_free_harmony_config.restype = None
    rcim_free_harmony_config.argtypes = [ctypes.POINTER(struct_RcimHarmonyConfig)]
except AttributeError:
    pass
try:
    rcim_malloc_msg_type = _libraries['FIXME_STUB'].rcim_malloc_msg_type
    rcim_malloc_msg_type.restype = ctypes.POINTER(struct_RcimMessageType)
    rcim_malloc_msg_type.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_msg_type = _libraries['FIXME_STUB'].rcim_free_msg_type
    rcim_free_msg_type.restype = None
    rcim_free_msg_type.argtypes = [ctypes.POINTER(struct_RcimMessageType)]
except AttributeError:
    pass
try:
    rcim_malloc_conversation = _libraries['FIXME_STUB'].rcim_malloc_conversation
    rcim_malloc_conversation.restype = ctypes.POINTER(struct_RcimConversation)
    rcim_malloc_conversation.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_conversation = _libraries['FIXME_STUB'].rcim_free_conversation
    rcim_free_conversation.restype = None
    rcim_free_conversation.argtypes = [ctypes.POINTER(struct_RcimConversation)]
except AttributeError:
    pass
try:
    rcim_malloc_conversation_identifier = _libraries['FIXME_STUB'].rcim_malloc_conversation_identifier
    rcim_malloc_conversation_identifier.restype = ctypes.POINTER(struct_RcimConversationIdentifier)
    rcim_malloc_conversation_identifier.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_conversation_identifier_c = _libraries['FIXME_STUB'].rcim_free_conversation_identifier_c
    rcim_free_conversation_identifier_c.restype = None
    rcim_free_conversation_identifier_c.argtypes = [ctypes.POINTER(struct_RcimConversationIdentifier)]
except AttributeError:
    pass
try:
    rcim_malloc_conversation_identifier_vec = _libraries['FIXME_STUB'].rcim_malloc_conversation_identifier_vec
    rcim_malloc_conversation_identifier_vec.restype = ctypes.POINTER(struct_RcimConversationIdentifier)
    rcim_malloc_conversation_identifier_vec.argtypes = [int32_t]
except AttributeError:
    pass
try:
    rcim_free_conversation_identifier_vec = _libraries['FIXME_STUB'].rcim_free_conversation_identifier_vec
    rcim_free_conversation_identifier_vec.restype = None
    rcim_free_conversation_identifier_vec.argtypes = [ctypes.POINTER(struct_RcimConversationIdentifier), int32_t]
except AttributeError:
    pass
try:
    rcim_malloc_sdk_version = _libraries['FIXME_STUB'].rcim_malloc_sdk_version
    rcim_malloc_sdk_version.restype = ctypes.POINTER(struct_RcimSDKVersion)
    rcim_malloc_sdk_version.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_sdk_version = _libraries['FIXME_STUB'].rcim_free_sdk_version
    rcim_free_sdk_version.restype = None
    rcim_free_sdk_version.argtypes = [ctypes.POINTER(struct_RcimSDKVersion)]
except AttributeError:
    pass
try:
    rcim_malloc_engine_builder_param = _libraries['FIXME_STUB'].rcim_malloc_engine_builder_param
    rcim_malloc_engine_builder_param.restype = ctypes.POINTER(struct_RcimEngineBuilderParam)
    rcim_malloc_engine_builder_param.argtypes = []
except AttributeError:
    pass
try:
    rcim_free_engine_builder_param = _libraries['FIXME_STUB'].rcim_free_engine_builder_param
    rcim_free_engine_builder_param.restype = None
    rcim_free_engine_builder_param.argtypes = [ctypes.POINTER(struct_RcimEngineBuilderParam)]
except AttributeError:
    pass
try:
    rcim_malloc_push_token_info_vec = _libraries['FIXME_STUB'].rcim_malloc_push_token_info_vec
    rcim_malloc_push_token_info_vec.restype = ctypes.POINTER(struct_RcimPushTokenInfo)
    rcim_malloc_push_token_info_vec.argtypes = [int32_t]
except AttributeError:
    pass
try:
    rcim_free_push_token_info_vec = _libraries['FIXME_STUB'].rcim_free_push_token_info_vec
    rcim_free_push_token_info_vec.restype = None
    rcim_free_push_token_info_vec.argtypes = [ctypes.POINTER(struct_RcimPushTokenInfo), int32_t]
except AttributeError:
    pass
try:
    rcim_free_char = _libraries['FIXME_STUB'].rcim_free_char
    rcim_free_char.restype = None
    rcim_free_char.argtypes = [ctypes.POINTER(ctypes.c_char)]
except AttributeError:
    pass
try:
    rcim_engine_set_cmp_send_listener = _libraries['FIXME_STUB'].rcim_engine_set_cmp_send_listener
    rcim_engine_set_cmp_send_listener.restype = RcimEngineError
    rcim_engine_set_cmp_send_listener.argtypes = [ctypes.POINTER(struct_RcimEngineSync), ctypes.POINTER(None), RcimCmpSendCb]
except AttributeError:
    pass
__all__ = \
    ['RcimAndroidConfig', 'RcimAppState', 'RcimAppState_Background',
    'RcimAppState_Foreground', 'RcimAppState_Hangup',
    'RcimAppState_Terminate', 'RcimAreaCode', 'RcimAreaCode_Bj',
    'RcimAreaCode_Na', 'RcimAreaCode_Sa', 'RcimAreaCode_Sg',
    'RcimAreaCode_SgB', 'RcimChatroomGetKvCb', 'RcimChatroomInfo',
    'RcimChatroomJoinedInfo', 'RcimChatroomKeyErrorInfo',
    'RcimChatroomKvCb', 'RcimChatroomKvChangedLsr',
    'RcimChatroomKvDeleteLsr', 'RcimChatroomKvInfo',
    'RcimChatroomKvSyncLsr', 'RcimChatroomMemberActionInfo',
    'RcimChatroomMemberActionType',
    'RcimChatroomMemberActionType_Join',
    'RcimChatroomMemberActionType_Quit',
    'RcimChatroomMemberBannedEventType',
    'RcimChatroomMemberBannedEventType_AddWhitelist',
    'RcimChatroomMemberBannedEventType_MuteAll',
    'RcimChatroomMemberBannedEventType_MuteGlobal',
    'RcimChatroomMemberBannedEventType_MuteUsers',
    'RcimChatroomMemberBannedEventType_RemoveWhitelist',
    'RcimChatroomMemberBannedEventType_UnmuteAll',
    'RcimChatroomMemberBannedEventType_UnmuteGlobal',
    'RcimChatroomMemberBannedEventType_UnmuteUser',
    'RcimChatroomMemberBannedInfo', 'RcimChatroomMemberBannedLsr',
    'RcimChatroomMemberBlockedEventType',
    'RcimChatroomMemberBlockedEventType_Block',
    'RcimChatroomMemberBlockedEventType_Unblock',
    'RcimChatroomMemberBlockedInfo', 'RcimChatroomMemberBlockedLsr',
    'RcimChatroomMemberChangeInfo', 'RcimChatroomMemberChangedLsr',
    'RcimChatroomMultiClientSyncEventType',
    'RcimChatroomMultiClientSyncEventType_Join',
    'RcimChatroomMultiClientSyncEventType_Quit',
    'RcimChatroomMultiClientSyncInfo',
    'RcimChatroomMultiClientSyncLsr',
    'RcimChatroomMultiClientSyncQuitType',
    'RcimChatroomMultiClientSyncQuitType_Kick',
    'RcimChatroomMultiClientSyncQuitType_Manual',
    'RcimChatroomStatus', 'RcimChatroomStatusLsr',
    'RcimChatroomStatus_DestroyAuto',
    'RcimChatroomStatus_DestroyManually', 'RcimChatroomStatus_Idle',
    'RcimChatroomStatus_JoinFailed', 'RcimChatroomStatus_Joined',
    'RcimChatroomStatus_Joining', 'RcimChatroomStatus_LeaveFailed',
    'RcimChatroomStatus_Leaving', 'RcimChatroomStatus_Left',
    'RcimChatroomUserInfo', 'RcimCloudType',
    'RcimCloudType_PrivateCloud', 'RcimCloudType_PrivateCloud104',
    'RcimCloudType_PublicCloud', 'RcimCmpSendCb', 'RcimCodeMessageCb',
    'RcimConnectCb', 'RcimConnectionStatus',
    'RcimConnectionStatusLsr', 'RcimConnectionStatus_Connected',
    'RcimConnectionStatus_Connecting',
    'RcimConnectionStatus_DisconnectAppAuthFailed',
    'RcimConnectionStatus_DisconnectAppBlockOrDelete',
    'RcimConnectionStatus_DisconnectClusterError',
    'RcimConnectionStatus_DisconnectConcurrentLimitError',
    'RcimConnectionStatus_DisconnectConnectionTimeout',
    'RcimConnectionStatus_DisconnectDatabaseOpenFailed',
    'RcimConnectionStatus_DisconnectDeviceError',
    'RcimConnectionStatus_DisconnectHostnameError',
    'RcimConnectionStatus_DisconnectIdReject',
    'RcimConnectionStatus_DisconnectIllegalProtocolVersion',
    'RcimConnectionStatus_DisconnectLicenseExpired',
    'RcimConnectionStatus_DisconnectLicenseMismatch',
    'RcimConnectionStatus_DisconnectNetworkUnavailable',
    'RcimConnectionStatus_DisconnectNotAuthorized',
    'RcimConnectionStatus_DisconnectOneTimePasswordUsed',
    'RcimConnectionStatus_DisconnectOtherDeviceLogin',
    'RcimConnectionStatus_DisconnectPackageNameInvalid',
    'RcimConnectionStatus_DisconnectPlatformError',
    'RcimConnectionStatus_DisconnectPlatformUnavailable',
    'RcimConnectionStatus_DisconnectTokenExpired',
    'RcimConnectionStatus_DisconnectTokenIncorrect',
    'RcimConnectionStatus_DisconnectUserBlocked',
    'RcimConnectionStatus_DisconnectUserDeleteAccount',
    'RcimConnectionStatus_DisconnectUserKicked',
    'RcimConnectionStatus_DisconnectUserLogout',
    'RcimConnectionStatus_Disconnecting', 'RcimConnectionStatus_Idle',
    'RcimConversation', 'RcimConversationIdentifier',
    'RcimConversationReadStatusLsr',
    'RcimConversationStatusChangeItem', 'RcimConversationStatusLsr',
    'RcimConversationType', 'RcimConversationType_AppPublicService',
    'RcimConversationType_Chatroom',
    'RcimConversationType_CustomerService',
    'RcimConversationType_Discussion',
    'RcimConversationType_Encrypted', 'RcimConversationType_Group',
    'RcimConversationType_NotSupportedYet',
    'RcimConversationType_Private',
    'RcimConversationType_PublicService',
    'RcimConversationType_PushService',
    'RcimConversationType_RtcRoom', 'RcimConversationType_System',
    'RcimConversationType_UltraGroup', 'RcimDatabaseStatus',
    'RcimDatabaseStatusLsr', 'RcimDatabaseStatus_Error',
    'RcimDatabaseStatus_Idle', 'RcimDatabaseStatus_OpenFailed',
    'RcimDatabaseStatus_OpenSuccess',
    'RcimDatabaseStatus_UpgradeFailed',
    'RcimDatabaseStatus_UpgradeSuccess',
    'RcimDatabaseStatus_Upgrading', 'RcimDevLogLevel',
    'RcimDevLogLevel_Debug', 'RcimDevLogLevel_Error',
    'RcimDevLogLevel_Info', 'RcimDevLogLevel_Trace',
    'RcimDevLogLevel_Warn', 'RcimDevLogLsr', 'RcimDisconnectMode',
    'RcimDisconnectMode_KeepPush', 'RcimDisconnectMode_NoPush',
    'RcimDownloadFileProgressCb', 'RcimDownloadMediaCb',
    'RcimDownloadMessageProgressCb', 'RcimEngineBuilder',
    'RcimEngineBuilderParam', 'RcimEngineError', 'RcimEngineErrorCb',
    'RcimEngineError_CallAlreadyJoinRoom',
    'RcimEngineError_CallAnswerInviteNotProgress',
    'RcimEngineError_CallAnswerInviteTimeout',
    'RcimEngineError_CallCancelInviteNotProgress',
    'RcimEngineError_CallConcurrentLimitError',
    'RcimEngineError_CallDbError', 'RcimEngineError_CallExpiredError',
    'RcimEngineError_CallGetTokenError',
    'RcimEngineError_CallHasNoConfigMcuAddress',
    'RcimEngineError_CallHasNoRoom',
    'RcimEngineError_CallIdentityChangeTypeError',
    'RcimEngineError_CallInternalError',
    'RcimEngineError_CallInvalidUserId',
    'RcimEngineError_CallInviteInProgress',
    'RcimEngineError_CallInviteRoomNotExist',
    'RcimEngineError_CallInviteUserNotInRoom',
    'RcimEngineError_CallJsonError', 'RcimEngineError_CallLimitError',
    'RcimEngineError_CallNoAuthUser',
    'RcimEngineError_CallNotAllowAudioBroadcast',
    'RcimEngineError_CallNotAllowCrossApp',
    'RcimEngineError_CallNotAllowVideoBroadcast',
    'RcimEngineError_CallNotInRoom', 'RcimEngineError_CallNotOpen',
    'RcimEngineError_CallParamError',
    'RcimEngineError_CallPingNotProgress',
    'RcimEngineError_CallRoomAlreadyExist',
    'RcimEngineError_CallRoomTypeError',
    'RcimEngineError_CallRoomTypeNotSupport',
    'RcimEngineError_CallTokenError',
    'RcimEngineError_CallUserIsBlocked',
    'RcimEngineError_CallUserNotAllowedForRtc',
    'RcimEngineError_CallplusAcceptNotAllowed',
    'RcimEngineError_CallplusAudioToVideoCancel',
    'RcimEngineError_CallplusAudioToVideoNoRequired',
    'RcimEngineError_CallplusCallNotExist',
    'RcimEngineError_CallplusCallNotSelf',
    'RcimEngineError_CallplusCallUserNotInCall',
    'RcimEngineError_CallplusCallingUserNotRegistCallServer',
    'RcimEngineError_CallplusCircuitBreakerOpen',
    'RcimEngineError_CallplusDataHasExpired',
    'RcimEngineError_CallplusDbError',
    'RcimEngineError_CallplusDeviceHasCalling',
    'RcimEngineError_CallplusGroupCallOverload',
    'RcimEngineError_CallplusHangupNotAllowed',
    'RcimEngineError_CallplusInvalidJsonFormat',
    'RcimEngineError_CallplusJsonError',
    'RcimEngineError_CallplusMediaTypeSwitching',
    'RcimEngineError_CallplusMethodNotImplement',
    'RcimEngineError_CallplusMissingParameters',
    'RcimEngineError_CallplusNoCompensationData',
    'RcimEngineError_CallplusNotSupportNewCall',
    'RcimEngineError_CallplusOperationHasExpired',
    'RcimEngineError_CallplusOperationNotAllowed',
    'RcimEngineError_CallplusOperationNotPermitted',
    'RcimEngineError_CallplusSingleCallOverload',
    'RcimEngineError_CallplusStateNotExist',
    'RcimEngineError_CallplusStreamReadyTimeInvalid',
    'RcimEngineError_CallplusTransactionNotExist',
    'RcimEngineError_CallplusUnknownError',
    'RcimEngineError_CallplusVideoToAudioNoRequired',
    'RcimEngineError_ChatroomInvalidParameter',
    'RcimEngineError_ChatroomIsFull',
    'RcimEngineError_ChatroomKicked',
    'RcimEngineError_ChatroomKvCallAPIExceed',
    'RcimEngineError_ChatroomKvConcurrentError',
    'RcimEngineError_ChatroomKvCountExceed',
    'RcimEngineError_ChatroomKvInvalidKey',
    'RcimEngineError_ChatroomKvInvalidKeyValueVec',
    'RcimEngineError_ChatroomKvInvalidKeyVec',
    'RcimEngineError_ChatroomKvInvalidValue',
    'RcimEngineError_ChatroomKvLimit',
    'RcimEngineError_ChatroomKvNotAllSuccess',
    'RcimEngineError_ChatroomKvNotExist',
    'RcimEngineError_ChatroomKvOverwriteInvalidKey',
    'RcimEngineError_ChatroomKvStoreUnavailable',
    'RcimEngineError_ChatroomNotExist',
    'RcimEngineError_CloudStorageForHistoryMessageDisable',
    'RcimEngineError_ConnectAppAuthFailed',
    'RcimEngineError_ConnectAppBlockOrDelete',
    'RcimEngineError_ConnectClusterError',
    'RcimEngineError_ConnectConcurrentLimitError',
    'RcimEngineError_ConnectDeviceError',
    'RcimEngineError_ConnectHostnameError',
    'RcimEngineError_ConnectIdReject',
    'RcimEngineError_ConnectIllegalProtocolVersion',
    'RcimEngineError_ConnectLicenseExpired',
    'RcimEngineError_ConnectNotAuthorized',
    'RcimEngineError_ConnectOneTimePasswordUsed',
    'RcimEngineError_ConnectOtherDeviceLogin',
    'RcimEngineError_ConnectPackageNameInvalid',
    'RcimEngineError_ConnectPlatformError',
    'RcimEngineError_ConnectPlatformUnavailable',
    'RcimEngineError_ConnectRedirect',
    'RcimEngineError_ConnectRefused',
    'RcimEngineError_ConnectTokenExpired',
    'RcimEngineError_ConnectTokenIncorrect',
    'RcimEngineError_ConnectUserBlocked',
    'RcimEngineError_ConnectUserDeleteAccount',
    'RcimEngineError_ConnectionCancel',
    'RcimEngineError_ConnectionClosed',
    'RcimEngineError_ConnectionClosing',
    'RcimEngineError_ConnectionExists',
    'RcimEngineError_ConnectionInProcess',
    'RcimEngineError_ConnectionTimeout',
    'RcimEngineError_ConversationNotSupportMessage',
    'RcimEngineError_DatabaseIOError',
    'RcimEngineError_DatabaseNotOpened',
    'RcimEngineError_DatabaseOpenFailed',
    'RcimEngineError_DatabaseTargetNotFound',
    'RcimEngineError_DatabaseThreadError',
    'RcimEngineError_DirectionalMessageNotSupport',
    'RcimEngineError_DisconnectUserBlocked',
    'RcimEngineError_DisconnectUserKicked',
    'RcimEngineError_DisconnectUserLogout',
    'RcimEngineError_DownloadRequestExist',
    'RcimEngineError_DownloadTaskNotExist',
    'RcimEngineError_EngineDropped',
    'RcimEngineError_ForbiddenInChatroom',
    'RcimEngineError_ForbiddenInGroupChat',
    'RcimEngineError_ForbiddenInPrivateChat',
    'RcimEngineError_GetUploadTokenError',
    'RcimEngineError_GetUserError',
    'RcimEngineError_GifMessageSizeOutOfLimit',
    'RcimEngineError_GroupReadReceiptVersionNotSupport',
    'RcimEngineError_HttpReqFailed', 'RcimEngineError_HttpReqTimeout',
    'RcimEngineError_ImageFormatError',
    'RcimEngineError_InvalidArgumentAppKey',
    'RcimEngineError_InvalidArgumentAppVersion',
    'RcimEngineError_InvalidArgumentAudioDuration',
    'RcimEngineError_InvalidArgumentChannelId',
    'RcimEngineError_InvalidArgumentChatroomId',
    'RcimEngineError_InvalidArgumentConnectionStatus',
    'RcimEngineError_InvalidArgumentContentNotMedia',
    'RcimEngineError_InvalidArgumentConversationIdentifierVec',
    'RcimEngineError_InvalidArgumentConversationType',
    'RcimEngineError_InvalidArgumentConversationTypeVec',
    'RcimEngineError_InvalidArgumentCount',
    'RcimEngineError_InvalidArgumentDestructDuration',
    'RcimEngineError_InvalidArgumentDeviceId',
    'RcimEngineError_InvalidArgumentDeviceManufacturer',
    'RcimEngineError_InvalidArgumentDeviceModel',
    'RcimEngineError_InvalidArgumentDraft',
    'RcimEngineError_InvalidArgumentEngineBuilder',
    'RcimEngineError_InvalidArgumentEngineBuilderParam',
    'RcimEngineError_InvalidArgumentEngineSync',
    'RcimEngineError_InvalidArgumentExtra',
    'RcimEngineError_InvalidArgumentFileNameEmpty',
    'RcimEngineError_InvalidArgumentFileStoragePath',
    'RcimEngineError_InvalidArgumentKeyword',
    'RcimEngineError_InvalidArgumentLimit',
    'RcimEngineError_InvalidArgumentLogInfo',
    'RcimEngineError_InvalidArgumentMediaLocalPath',
    'RcimEngineError_InvalidArgumentMediaUrl',
    'RcimEngineError_InvalidArgumentMessage',
    'RcimEngineError_InvalidArgumentMessageContent',
    'RcimEngineError_InvalidArgumentMessageDirection',
    'RcimEngineError_InvalidArgumentMessageDirectionEmpty',
    'RcimEngineError_InvalidArgumentMessageId',
    'RcimEngineError_InvalidArgumentMessageIdVec',
    'RcimEngineError_InvalidArgumentMessageType',
    'RcimEngineError_InvalidArgumentMessageUid',
    'RcimEngineError_InvalidArgumentMessageVec',
    'RcimEngineError_InvalidArgumentNaviUrl',
    'RcimEngineError_InvalidArgumentNotMediaMessage',
    'RcimEngineError_InvalidArgumentObjectName',
    'RcimEngineError_InvalidArgumentObjectNameVec',
    'RcimEngineError_InvalidArgumentOffset',
    'RcimEngineError_InvalidArgumentOsVersion',
    'RcimEngineError_InvalidArgumentOutUniqueId',
    'RcimEngineError_InvalidArgumentOutUserId',
    'RcimEngineError_InvalidArgumentPackageName',
    'RcimEngineError_InvalidArgumentPushNotificationMuteLevel',
    'RcimEngineError_InvalidArgumentPushNotificationMuteLevelVec',
    'RcimEngineError_InvalidArgumentPushToken',
    'RcimEngineError_InvalidArgumentPushTokenVec',
    'RcimEngineError_InvalidArgumentPushType',
    'RcimEngineError_InvalidArgumentRtcKey',
    'RcimEngineError_InvalidArgumentRtcMethodName',
    'RcimEngineError_InvalidArgumentRtcValue',
    'RcimEngineError_InvalidArgumentSdkVersion',
    'RcimEngineError_InvalidArgumentSenderId',
    'RcimEngineError_InvalidArgumentSentStatus',
    'RcimEngineError_InvalidArgumentSpanMinutes',
    'RcimEngineError_InvalidArgumentStatisticUrl',
    'RcimEngineError_InvalidArgumentTargetId',
    'RcimEngineError_InvalidArgumentTimeInterval',
    'RcimEngineError_InvalidArgumentTimeString',
    'RcimEngineError_InvalidArgumentTimeoutSeconds',
    'RcimEngineError_InvalidArgumentTimestamp',
    'RcimEngineError_InvalidArgumentToken',
    'RcimEngineError_InvalidArgumentUltraGroupNotSupport',
    'RcimEngineError_InvalidArgumentUniqueId',
    'RcimEngineError_InvalidArgumentUserIdEmpty',
    'RcimEngineError_InvalidArgumentVersion',
    'RcimEngineError_InvalidEnumOutOfRange',
    'RcimEngineError_InvalidParameterMessageExpansion',
    'RcimEngineError_InvalidParameterReceivedStatus',
    'RcimEngineError_InvalidParameterUserId',
    'RcimEngineError_InvalidParameterUserList',
    'RcimEngineError_InvalidPublicService',
    'RcimEngineError_JsonParserFailed',
    'RcimEngineError_KvStoreIOError',
    'RcimEngineError_KvStoreNotOpened',
    'RcimEngineError_KvStoreOpenFailed',
    'RcimEngineError_KvStoreSerializationError',
    'RcimEngineError_MediaMessageHandlerError',
    'RcimEngineError_MessageCantExpand',
    'RcimEngineError_MessageDestructing',
    'RcimEngineError_MessageExpandConversationTypeNotMatch',
    'RcimEngineError_MessageExpansionSizeLimitExceed',
    'RcimEngineError_MessageIncludeSensitiveWord',
    'RcimEngineError_MessageNotDestructing',
    'RcimEngineError_MessageNotRegistered',
    'RcimEngineError_MessageReplacedSensitiveWord',
    'RcimEngineError_MessageSavedError',
    'RcimEngineError_MessageSendOverFrequency',
    'RcimEngineError_MessageStorageServiceUnavailable',
    'RcimEngineError_MsgSizeOutOfLimit',
    'RcimEngineError_NaviLicenseMismatch',
    'RcimEngineError_NaviReqFailed', 'RcimEngineError_NaviReqTimeout',
    'RcimEngineError_NaviRespTokenIncorrect',
    'RcimEngineError_NetDataParserFailed',
    'RcimEngineError_NotInChatroom', 'RcimEngineError_NotInGroup',
    'RcimEngineError_NotSupportedYet',
    'RcimEngineError_NotWhitelisted',
    'RcimEngineError_PushSettingParameterInvalid',
    'RcimEngineError_QueryChatroomHistoryError',
    'RcimEngineError_RecallMessageUserInvalid',
    'RcimEngineError_RecallParameterInvalid',
    'RcimEngineError_RejectedByBlackList',
    'RcimEngineError_RequestCanceled',
    'RcimEngineError_RequestOverFrequency',
    'RcimEngineError_RequestPaused',
    'RcimEngineError_RequestUploadTokenError',
    'RcimEngineError_RequestUploadTokenSizeError',
    'RcimEngineError_RoamingServiceUnavailableChatroom',
    'RcimEngineError_SettingSyncFailed',
    'RcimEngineError_SightMessageCompressError',
    'RcimEngineError_SightMsgDurationLimit',
    'RcimEngineError_SocketConnectionFailed',
    'RcimEngineError_SocketRecvTimeout',
    'RcimEngineError_SocketSendTimeout',
    'RcimEngineError_SocketShutdownFailed', 'RcimEngineError_Success',
    'RcimEngineError_UploadMediaFailed',
    'RcimEngineError_UploadTaskNotExist',
    'RcimEngineError_UserSettingUnavailable', 'RcimEngineSync',
    'RcimGetBoolCb', 'RcimGetChatroomInfoCb', 'RcimGetConversationCb',
    'RcimGetConversationListCb', 'RcimGetCountCb',
    'RcimGetLocalConversationMuteLevelCb',
    'RcimGetLocalPublicServiceListCb', 'RcimGetMessageListCb',
    'RcimGetNoDisturbingCb', 'RcimGetPublicServiceCb',
    'RcimGetReadReceiptV2ReaderListCb', 'RcimGetTextMessageDraftCb',
    'RcimHarmonyConfig', 'RcimInsertLogInfo', 'RcimIosConfig',
    'RcimJoinChatroomCb', 'RcimJoinExistingChatroomCb', 'RcimLogInfo',
    'RcimLogLevel', 'RcimLogLevel_Debug', 'RcimLogLevel_Error',
    'RcimLogLevel_Info', 'RcimLogLevel_None', 'RcimLogLevel_Warn',
    'RcimLogLsr', 'RcimLogSource', 'RcimLogSource_CallLib',
    'RcimLogSource_CallPlus', 'RcimLogSource_FFI',
    'RcimLogSource_IMKit', 'RcimLogSource_IMLib',
    'RcimLogSource_RTCLib', 'RcimLogSource_RUST', 'RcimLogType',
    'RcimLogType_IM', 'RcimLogType_RTC', 'RcimMediaHandlerError',
    'RcimMediaHandlerError_Canceled', 'RcimMediaHandlerError_Failed',
    'RcimMediaHandlerError_Paused', 'RcimMediaHandlerError_Success',
    'RcimMediaHandlerProgressCb', 'RcimMediaHandlerResultCb',
    'RcimMediaMessageHandlerCb', 'RcimMessageBlockInfo',
    'RcimMessageBlockSourceType',
    'RcimMessageBlockSourceType_Default',
    'RcimMessageBlockSourceType_Extension',
    'RcimMessageBlockSourceType_Modification', 'RcimMessageBlockType',
    'RcimMessageBlockType_BlockCustom',
    'RcimMessageBlockType_BlockGlobal',
    'RcimMessageBlockType_BlockThirdParty',
    'RcimMessageBlockType_None', 'RcimMessageBlockedLsr',
    'RcimMessageBox', 'RcimMessageCb', 'RcimMessageDestructingLsr',
    'RcimMessageDestructionStopLsr', 'RcimMessageDirection',
    'RcimMessageDirection_Receive', 'RcimMessageDirection_Send',
    'RcimMessageExpansionKvInfo', 'RcimMessageExpansionKvRemoveLsr',
    'RcimMessageExpansionKvUpdateLsr', 'RcimMessageFlag',
    'RcimMessageFlag_Count', 'RcimMessageFlag_None',
    'RcimMessageFlag_Save', 'RcimMessageFlag_Status',
    'RcimMessageNotifyLsr', 'RcimMessageReceivedLsr',
    'RcimMessageSearchableWordsCb', 'RcimMessageSearchableWordsCbLsr',
    'RcimMessageType', 'RcimNetworkType',
    'RcimNetworkType_Cellular2G', 'RcimNetworkType_Cellular3G',
    'RcimNetworkType_Cellular4G', 'RcimNetworkType_Cellular5G',
    'RcimNetworkType_None', 'RcimNetworkType_Wifi',
    'RcimNetworkType_Wired', 'RcimOfflineMessageSyncCompletedLsr',
    'RcimOrder', 'RcimOrder_Ascending', 'RcimOrder_Descending',
    'RcimPlatform', 'RcimPlatform_Android', 'RcimPlatform_Electron',
    'RcimPlatform_HarmonyOS', 'RcimPlatform_IOS',
    'RcimPlatform_Linux', 'RcimPlatform_MacOS',
    'RcimPlatform_Unknown', 'RcimPlatform_Web',
    'RcimPlatform_Windows', 'RcimPublicServiceInfo',
    'RcimPublicServiceMenuItem', 'RcimPublicServiceMenuItemType',
    'RcimPublicServiceMenuItemType_Click',
    'RcimPublicServiceMenuItemType_Group',
    'RcimPublicServiceMenuItemType_View', 'RcimPushConfig',
    'RcimPushNotificationMuteLevel',
    'RcimPushNotificationMuteLevel_All',
    'RcimPushNotificationMuteLevel_Blocked',
    'RcimPushNotificationMuteLevel_Default',
    'RcimPushNotificationMuteLevel_Mention',
    'RcimPushNotificationMuteLevel_MentionAll',
    'RcimPushNotificationMuteLevel_MentionUsers', 'RcimPushTokenInfo',
    'RcimReadReceiptInfo', 'RcimReadReceiptInfoV2',
    'RcimReadReceiptRequestLsr', 'RcimReadReceiptResponseLsr',
    'RcimReadReceiptResponseV2Lsr', 'RcimReadReceiptUserInfo',
    'RcimReadReceiptV2ReaderInfo', 'RcimRecallMessageCb',
    'RcimRecallMessageLsr', 'RcimRecallNotificationMessage',
    'RcimReceivedInfo', 'RcimReceivedStatus', 'RcimRtcConfig',
    'RcimRtcHeartBeatResultLsr', 'RcimRtcHeartBeatSendLsr',
    'RcimRtcKvInfo', 'RcimRtcKvSignalingLsr', 'RcimRtcRoomEventLsr',
    'RcimRtcSetKVSignalingCb', 'RcimSDKVersion',
    'RcimSendMessageOnProgressCb', 'RcimSendMessageOption',
    'RcimSendReadReceiptResponseMessageData',
    'RcimSendRtcSignalingCb', 'RcimSentStatus',
    'RcimSentStatus_CANCELED', 'RcimSentStatus_DESTROYED',
    'RcimSentStatus_FAILED', 'RcimSentStatus_READ',
    'RcimSentStatus_RECEIVED', 'RcimSentStatus_SENDING',
    'RcimSentStatus_SENT', 'RcimSightCompressCb',
    'RcimSightCompressCbLsr', 'RcimTypingStatus',
    'RcimTypingStatusLsr', 'RcimVoipCallInfoLsr', 'int32_t',
    'int64_t', 'rcim_create_engine_builder', 'rcim_destroy_engine',
    'rcim_destroy_engine_builder', 'rcim_dev_log_init',
    'rcim_engine_builder_build', 'rcim_engine_builder_set_area_code',
    'rcim_engine_builder_set_cloud_type',
    'rcim_engine_builder_set_db_encrypted',
    'rcim_engine_builder_set_enable_group_call',
    'rcim_engine_builder_set_enable_reconnect_kick',
    'rcim_engine_builder_set_file_path',
    'rcim_engine_builder_set_navi_server',
    'rcim_engine_builder_set_network_env',
    'rcim_engine_builder_set_statistic_server',
    'rcim_engine_builder_set_store_path',
    'rcim_engine_cancel_download_file',
    'rcim_engine_cancel_download_media_message',
    'rcim_engine_cancel_rtc_signaling',
    'rcim_engine_cancel_send_media_message',
    'rcim_engine_clean_local_history_messages',
    'rcim_engine_clean_remote_history_messages',
    'rcim_engine_clear_local_conversations',
    'rcim_engine_clear_messages_unread_status',
    'rcim_engine_clear_messages_unread_status_by_send_time',
    'rcim_engine_connect', 'rcim_engine_delete_chatroom_kvs',
    'rcim_engine_delete_local_messages',
    'rcim_engine_delete_local_messages_by_ids',
    'rcim_engine_delete_remote_messages', 'rcim_engine_disconnect',
    'rcim_engine_download_file_with_progress',
    'rcim_engine_download_file_with_unique_id',
    'rcim_engine_download_media_message',
    'rcim_engine_get_chatroom_all_kvs',
    'rcim_engine_get_chatroom_info',
    'rcim_engine_get_connection_status', 'rcim_engine_get_delta_time',
    'rcim_engine_get_first_unread_message',
    'rcim_engine_get_local_all_public_services',
    'rcim_engine_get_local_chatroom_kv_by_keys',
    'rcim_engine_get_local_conversation',
    'rcim_engine_get_local_conversation_mute_level',
    'rcim_engine_get_local_conversation_pin_status',
    'rcim_engine_get_local_conversations_by_page',
    'rcim_engine_get_local_history_messages_by_id',
    'rcim_engine_get_local_history_messages_by_senders',
    'rcim_engine_get_local_history_messages_by_time',
    'rcim_engine_get_local_message_by_id',
    'rcim_engine_get_local_message_by_uid',
    'rcim_engine_get_local_muted_conversations_by_page',
    'rcim_engine_get_local_pin_conversations_by_page',
    'rcim_engine_get_local_public_service',
    'rcim_engine_get_local_unread_conversation',
    'rcim_engine_get_no_disturbing',
    'rcim_engine_get_push_content_show_status',
    'rcim_engine_get_push_receive_status',
    'rcim_engine_get_read_receipt_v2_readers',
    'rcim_engine_get_remote_history_messages',
    'rcim_engine_get_sdk_version',
    'rcim_engine_get_text_message_draft',
    'rcim_engine_get_total_unread_count',
    'rcim_engine_get_unread_count',
    'rcim_engine_get_unread_count_by_conversation_types',
    'rcim_engine_get_unread_count_by_conversations',
    'rcim_engine_get_unread_mentioned_messages',
    'rcim_engine_get_user_id', 'rcim_engine_insert_local_message',
    'rcim_engine_insert_local_messages', 'rcim_engine_insert_log',
    'rcim_engine_join_chatroom', 'rcim_engine_join_existing_chatroom',
    'rcim_engine_message_begin_destruct',
    'rcim_engine_message_stop_destruct',
    'rcim_engine_mute_conversations',
    'rcim_engine_notify_app_state_changed',
    'rcim_engine_notify_network_changed',
    'rcim_engine_pause_download_file',
    'rcim_engine_pause_download_media_message',
    'rcim_engine_pin_conversations', 'rcim_engine_quit_chatroom',
    'rcim_engine_recall_message',
    'rcim_engine_register_message_types',
    'rcim_engine_remove_conversations',
    'rcim_engine_remove_message_expansion',
    'rcim_engine_rtc_set_kv_signaling',
    'rcim_engine_save_text_message_draft',
    'rcim_engine_search_local_conversations',
    'rcim_engine_search_local_messages',
    'rcim_engine_search_local_messages_by_multiple_conversations',
    'rcim_engine_search_local_messages_by_object_name',
    'rcim_engine_search_local_messages_by_time',
    'rcim_engine_search_local_messages_by_user_id',
    'rcim_engine_send_media_message', 'rcim_engine_send_message',
    'rcim_engine_send_read_receipt_message',
    'rcim_engine_send_read_receipt_request',
    'rcim_engine_send_read_receipt_response',
    'rcim_engine_send_read_receipt_response_v2',
    'rcim_engine_send_rtc_heartbeat',
    'rcim_engine_send_rtc_signaling',
    'rcim_engine_send_typing_status',
    'rcim_engine_set_chatroom_kv_changed_listener',
    'rcim_engine_set_chatroom_kv_delete_listener',
    'rcim_engine_set_chatroom_kv_sync_listener',
    'rcim_engine_set_chatroom_kvs',
    'rcim_engine_set_chatroom_member_banned_listener',
    'rcim_engine_set_chatroom_member_blocked_listener',
    'rcim_engine_set_chatroom_member_changed_listener',
    'rcim_engine_set_chatroom_multi_client_sync_listener',
    'rcim_engine_set_chatroom_status_listener',
    'rcim_engine_set_cmp_send_listener',
    'rcim_engine_set_connection_status_listener',
    'rcim_engine_set_conversation_status_listener',
    'rcim_engine_set_database_status_listener',
    'rcim_engine_set_device_id', 'rcim_engine_set_log_filter',
    'rcim_engine_set_log_listener',
    'rcim_engine_set_message_blocked_listener',
    'rcim_engine_set_message_content',
    'rcim_engine_set_message_destructing_listener',
    'rcim_engine_set_message_destruction_stop_listener',
    'rcim_engine_set_message_expansion_remove_listener',
    'rcim_engine_set_message_expansion_update_listener',
    'rcim_engine_set_message_extra',
    'rcim_engine_set_message_recalled_listener',
    'rcim_engine_set_message_received_listener',
    'rcim_engine_set_message_received_status',
    'rcim_engine_set_message_searchable_words_callback_listener',
    'rcim_engine_set_message_sent_status',
    'rcim_engine_set_no_disturbing',
    'rcim_engine_set_offline_message_sync_completed_listener',
    'rcim_engine_set_push_content_show_status',
    'rcim_engine_set_push_receive_status',
    'rcim_engine_set_push_token',
    'rcim_engine_set_read_receipt_received_listener',
    'rcim_engine_set_read_receipt_request_listener',
    'rcim_engine_set_read_receipt_response_listener',
    'rcim_engine_set_read_receipt_response_v2_listener',
    'rcim_engine_set_rtc_heartbeat_send_listener',
    'rcim_engine_set_rtc_heartbeat_send_result_listener',
    'rcim_engine_set_rtc_kv_signaling_listener',
    'rcim_engine_set_rtc_room_event_listener',
    'rcim_engine_set_sight_compress_callback_listener',
    'rcim_engine_set_sync_conversation_read_status_listener',
    'rcim_engine_set_typing_status_interval',
    'rcim_engine_set_typing_status_listener',
    'rcim_engine_set_voip_call_info_listener',
    'rcim_engine_sync_conversation_read_status',
    'rcim_engine_unset_no_disturbing',
    'rcim_engine_update_message_expansion',
    'rcim_free_android_config', 'rcim_free_char',
    'rcim_free_conversation', 'rcim_free_conversation_identifier_c',
    'rcim_free_conversation_identifier_vec',
    'rcim_free_engine_builder_param', 'rcim_free_harmony_config',
    'rcim_free_ios_config', 'rcim_free_message_box',
    'rcim_free_message_box_vec', 'rcim_free_msg_type',
    'rcim_free_push_config', 'rcim_free_push_token_info_vec',
    'rcim_free_receive_status', 'rcim_free_sdk_version',
    'rcim_malloc_android_config', 'rcim_malloc_conversation',
    'rcim_malloc_conversation_identifier',
    'rcim_malloc_conversation_identifier_vec',
    'rcim_malloc_engine_builder_param', 'rcim_malloc_harmony_config',
    'rcim_malloc_ios_config', 'rcim_malloc_message_box',
    'rcim_malloc_message_box_vec', 'rcim_malloc_msg_type',
    'rcim_malloc_push_config', 'rcim_malloc_push_token_info_vec',
    'rcim_malloc_receive_status', 'rcim_malloc_sdk_version',
    'struct_RcimAndroidConfig', 'struct_RcimChatroomInfo',
    'struct_RcimChatroomJoinedInfo',
    'struct_RcimChatroomKeyErrorInfo', 'struct_RcimChatroomKvInfo',
    'struct_RcimChatroomMemberActionInfo',
    'struct_RcimChatroomMemberBannedInfo',
    'struct_RcimChatroomMemberBlockedInfo',
    'struct_RcimChatroomMemberChangeInfo',
    'struct_RcimChatroomMultiClientSyncInfo',
    'struct_RcimChatroomUserInfo', 'struct_RcimConversation',
    'struct_RcimConversationIdentifier',
    'struct_RcimConversationStatusChangeItem',
    'struct_RcimEngineBuilder', 'struct_RcimEngineBuilderParam',
    'struct_RcimEngineSync', 'struct_RcimHarmonyConfig',
    'struct_RcimInsertLogInfo', 'struct_RcimIosConfig',
    'struct_RcimLogInfo', 'struct_RcimMessageBlockInfo',
    'struct_RcimMessageBox', 'struct_RcimMessageExpansionKvInfo',
    'struct_RcimMessageType', 'struct_RcimPublicServiceInfo',
    'struct_RcimPublicServiceMenuItem', 'struct_RcimPushConfig',
    'struct_RcimPushTokenInfo', 'struct_RcimReadReceiptInfo',
    'struct_RcimReadReceiptInfoV2', 'struct_RcimReadReceiptUserInfo',
    'struct_RcimReadReceiptV2ReaderInfo',
    'struct_RcimRecallNotificationMessage', 'struct_RcimReceivedInfo',
    'struct_RcimReceivedStatus', 'struct_RcimRtcConfig',
    'struct_RcimRtcKvInfo', 'struct_RcimSDKVersion',
    'struct_RcimSendMessageOption',
    'struct_RcimSendReadReceiptResponseMessageData',
    'struct_RcimTypingStatus']
