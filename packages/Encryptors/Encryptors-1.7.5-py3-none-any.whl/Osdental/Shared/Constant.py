from enum import Enum

class Constant(str,Enum):
    USER_TOKEN = 'user_token'
    AES_DATA = 'aes_data'
    DEFAULT_ENCODING = 'utf-8'
    MESSAGE_LOG_INTERNAL = 'MESSAGE_LOG_INTERNAL'
    DEFAULT_EMPTY_VALUE = '*'
    RESPONSE_TYPE_ERROR = 'ERROR'
    RESPONSE_TYPE_REQUEST = 'REQUEST'
    RESPONSE_TYPE_RESPONSE = 'RESPONSE'
    MESSAGE_LOG_EXTERNAL = 'MESSAGE_LOG_EXTERNAL'

    def __str__(self):
        return self.value