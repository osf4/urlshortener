from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone

import jwt

class Auth:
    """
    Provide methods to create & verify password and JWT tokens
    """
    
    def __init__(self, 
                 secret_key: str, 
                 access_token_expires_delta: timedelta,
                 algorithm = 'HS256'):
        
        self.algorithm = algorithm
        self.access_token_expires_delta = access_token_expires_delta

        self.__secret_key = secret_key
        self.__pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')


    def verify_password(self, plain: str | bytes, hashed: str | bytes) -> bool:
        """
        Return True, if the hash of 'plain' is the same as 'hashed'
        """
        
        return self.__pwd_context.verify(plain, hashed)
    

    def hash_password(self, plain: str | bytes) -> str:
        """
        Return the hash of the provided password
        """

        return self.__pwd_context.hash(plain)

    
    def create_access_token(self, 
                            username: str, 
                            expires_delta: timedelta | None = None) -> str:
        """
        Create the access token with 'sub': username and 'exp': expires_delta
        """
        
        expire = self.__expires_delta_or_default(expires_delta)
        to_encode = {'sub': username, 'exp': expire}

        return jwt.encode(to_encode, self.__secret_key, self.algorithm)

    
    def get_user_by_access_token(self, access_token: str) -> str:
        """
        Verify the access token and return the owner's username

        Raise ExpiredSignatureError, if the token is expired
        """
        
        payload = jwt.decode(access_token, self.__secret_key, algorithms = [self.algorithm])                    
        return payload['sub']

    
    def __expires_delta_or_default(self, expires_delta: timedelta | None) -> timedelta:
        """
        Return 'exp' field for token using the provided expires_delta or self.access_token_expires_delta

        """

        if not expires_delta:
            return datetime.now(timezone.utc) + self.access_token_expires_delta
        
        return datetime.now(timezone.utc) + expires_delta