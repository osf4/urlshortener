from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base model for all users
    """
    
    username: str


class UserInfo(UserBase):
    """
    Represent full user information
    """
    
    owned_urls: list[str] 


class UserRegisterIn(UserBase):
    """
    User registartion request
    """
    
    password: str


class UserRegisterOut(UserBase):
    """
    User registration reply
    """
    
    pass