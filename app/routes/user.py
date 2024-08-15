from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.models import User
from app.db.exceptions import UserExistsError

from app.schemas.user import UserInfo, UserRegisterIn, UserRegisterOut
from app.schemas.token import AccessToken

from app.dependencies import AuthDependency, CurrentUserDependency, StorageDependency


router = APIRouter(
    prefix = '/user',
    tags = ['User'],
)


async def authenticate_user(username: str, 
                            password: str,
                            auth: AuthDependency,
                            storage: StorageDependency) -> bool:
    
    user = await storage.get_user(username)
    if not user:
        return False
    
    return auth.verify_password(password, user.hashed_password)


@router.get('/me')
async def get_me(current_user: CurrentUserDependency) -> UserInfo:
    return current_user    


@router.post('/regist')
async def create_user(user: UserRegisterIn,
                      storage: StorageDependency,
                      auth: AuthDependency) -> UserRegisterOut:

    new_user = User(username = user.username, 
                    hashed_password = auth.hash_password(user.password))
    
    try:
        await storage.create_user(new_user)

    except UserExistsError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'The user already exists'
        )
    
    return user


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 auth: AuthDependency,
                                 storage: StorageDependency):
    
    authenticated = await authenticate_user(form_data.username,
                                            form_data.password,
                                            auth, 
                                            storage)
    
    if not authenticated:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    access_token = auth.create_access_token(form_data.username)
    return AccessToken(access_token = access_token)