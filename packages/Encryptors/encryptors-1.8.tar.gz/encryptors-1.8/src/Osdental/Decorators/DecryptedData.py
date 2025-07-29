import inspect
from functools import wraps
from typing import Callable
from Osdental.Encryptor.Jwt import JWT
from Osdental.Exception.ControlledException import UnauthorizedException
from Osdental.Handlers.DBSecurityQuery import DBSecurityQuery
from Osdental.Handlers.Instances import jwt_user_key, aes
from Osdental.Models.Token import AuthToken
from Osdental.Shared.Message import Message

db_security_query = DBSecurityQuery()

def process_encrypted_data():
    def decorator(func:Callable):
        @wraps(func)
        async def wrapper(self, user_token_encrypted:str = None, aes_data:str = None, **rest_kwargs): 
            legacy = await db_security_query.get_legacy_data()
            token = None
            if user_token_encrypted:
                user_token = aes.decrypt(legacy.aes_key_user, user_token_encrypted)
                token = AuthToken.from_jwt(JWT.extract_payload(user_token, jwt_user_key), legacy, jwt_user_key)
                is_auth = await db_security_query.validate_auth_token(token.id_token, token.id_user)
                if not is_auth:
                    raise UnauthorizedException(message=Message.PORTAL_ACCESS_RESTRICTED_MSG, error=Message.PORTAL_ACCESS_RESTRICTED_MSG)

            data = None
            if aes_data:
                decrypted_data = aes.decrypt(legacy.aes_key_auth, aes_data)
                data = decrypted_data

            sig = inspect.signature(func)
            kwargs_to_pass = {}
            if 'token' in sig.parameters:
                kwargs_to_pass['token'] = token
            if 'data' in sig.parameters:
                kwargs_to_pass['data'] = data

            return await func(self, **kwargs_to_pass, **rest_kwargs)
        
        return wrapper
    return decorator