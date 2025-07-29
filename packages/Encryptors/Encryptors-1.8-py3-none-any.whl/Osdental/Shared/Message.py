from enum import Enum

class Message(str,Enum):
    UNEXPECTED_ERROR_MSG = 'Something went wrong while processing your request. Please try again later.'
    PORTAL_ACCESS_RESTRICTED_MSG = 'You are not authorized to access this portal.'
    PROCESS_SUCCESS_MSG = 'Process executed successfully.'
    NO_RESULTS_FOUND_MSG = 'No records were found matching your request.'
    INVALID_REQUEST_PARAMS_MSG = 'Please review the required fields and try again.'
    SERVER_NETWORK_ACCESS_ERROR_MSG = 'Error making the server accessible on the network.'
    HEXAGONAL_SERVICE_CREATED_MSG = 'The hexagonal service structure was created.'
    PYCACHE_CLEANUP_SUCCESS_MSG = 'All __pycache__ have been removed.'
    NO_PASSWORD_CHARACTERS_MSG = 'There are no characters available to generate the password.'
    INSUFFICIENT_LENGTH_MSG = 'Insufficient length to meet minimum rules.'
    LEGACY_NAME_REQUIRED_MSG = 'Legacy name cannot be empty.'
    REFRESH_TOKEN_EXP_REQUIRED_MSG = 'Refresh token expiration time cannot be empty.'
    ACCESS_TOKEN_EXP_REQUIRED_MSG = 'Access token expiration time cannot be empty.'
    PUBLIC_KEY2_REQUIRED_MSG = 'Public key 2 cannot be empty.'
    PRIVATE_KEY1_REQUIRED_MSG = 'Private key 1 cannot be empty.'
    PRIVATE_KEY2_REQUIRED_MSG = 'Private key 2 cannot be empty.'
    AES_KEY_USER_REQUIRED_MSG = 'AES key user cannot be empty.'
    AES_KEY_AUTH_REQUIRED_MSG = 'AES key auth cannot be empty.'
    MISSING_FIELD_ERROR_MSG = 'A required field is missing. Please review the data.'

    def __str__(self):
        return self.value