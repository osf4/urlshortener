from dataclasses import dataclass
from typing import Annotated

from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserInfo
from app.config import Config

from app.db.models import User
from app.db.base_storage import BaseStorage
from app.db.mongo_storage import MongoStorage

from app.auth.auth import Auth


@dataclass
class AppDependencies:
    """
    Global dependencies for the application (authenticator and database)
    """
    
    auth: Auth
    storage: BaseStorage


    def get_auth(self) -> Auth:
        return self.auth


    def get_storage(self) -> BaseStorage:
        return self.storage


def init_dependencies() -> AppDependencies:
    """
    Load config from 'config.yaml' file
    """
    
    config = Config.load()
    
    auth = Auth(config.jwt.secret_key, 
                config.jwt.access_token_expire_time,
                config.jwt.algorithm)
    
    storage = MongoStorage(config.database.host,
                           config.database.port,
                           config.database.name)

    return AppDependencies(auth, storage)


app_dependencies = init_dependencies()
o2auth_scheme = OAuth2PasswordBearer(tokenUrl = '/user/token')

AuthDependency = Annotated[Auth, Depends(app_dependencies.get_auth)]
StorageDependency = Annotated[BaseStorage, Depends(app_dependencies.get_storage)]
TokenDependency = Annotated[str, Depends(o2auth_scheme)]


async def get_current_user(token: TokenDependency,
                           auth: AuthDependency,
                           storage: StorageDependency) -> UserInfo:
    """
    Parse the JWT token and return the user from DB

    Raise HTTPException, if the token is expired or can not be decoded
    """
    
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credentials',
        headers = {'WWW-Authenticate': 'Bearer'},
    )

    try:
        username = auth.get_user_by_access_token(token)
        if not await storage.user_exists(username):
            raise credentials_exception
        
        return await storage.get_user(username)
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Your access token is expired. Log in to get the new one!',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    except InvalidTokenError:
        raise credentials_exception
    

CurrentUserDependency = Annotated[User, Depends(get_current_user)]