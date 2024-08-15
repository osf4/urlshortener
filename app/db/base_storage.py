from abc import ABC, abstractmethod
from .models import User, Url

class BaseStorage(ABC):
    """
    Base storage for users and URLs
    """
    
    @abstractmethod
    async def create_user(self, user: User):
        """
        Create a new user.

        Raise UserExistsError, if the user with provided username already exists
        """
        
        pass


    @abstractmethod
    async def get_user(self, username: str) -> User | None:
        """
        Return a user by username.

        If the user was not found, None is returned
        """
        
        pass

    
    @abstractmethod
    async def delete_user(self, username: str):
        """
        Delete a user by username.

        Raise UserNotExistError, if the user does not exist
        """
        
        pass
    

    @abstractmethod
    async def user_exists(self, username: str) -> bool:
        """
        Return True, if the user with that username exists
        """
        
        pass
    

    @abstractmethod
    async def create_url(self,
                         *, 
                         owner_username: str, 
                         original_url: str, 
                         internal_url: str):
        """
        Create a URL by provided parameters.

        Raise UserNotExistError, if the user does not exist and UrlExistsError,
        if the URL with provided 'internal_url' already exists
        """
        
        pass


    @abstractmethod
    async def get_url(self, internal_url: str) -> Url | None:
        """
        Return a URL by 'internal_url' or None, if the URL does not exist
        """
        
        pass


    @abstractmethod
    async def get_url_owner(self, internal_url: str) -> str:
        """
        Return the owner of the URL with provided 'internal_url'.

        Raise UrlNotExistError, if the URL does not exist
        """
        
        pass


    @abstractmethod
    async def get_original_url(self, internal_url: str) -> str:
        """
        Return the 'original_url' for provided 'internal_url'

        Raise UrlNotExistError, if the URL does not exist
        """
        
        pass
    
    
    @abstractmethod
    async def enable_url(self, internal_url: str):
        """
        Set True to the 'active' field

        Raise UrlNotExistError, if the URL does not exist
        """
        
        pass


    @abstractmethod
    async def disable_url(self, internal_url: str):
        """
        Set False to the 'active' field

        Raise UrlNotExistError, if the URL does not exist
        """
        
        pass

    
    @abstractmethod
    async def delete_url(self, internal_url: str):
        """
        Delete the URL with provided 'internal_url'

        Raise UrlNotExistError, if the URL does not exist
        """
        
        pass

    
    @abstractmethod
    async def url_exists(self, internal_url: str) -> bool:
        """
        Return True, if the URL with provided 'internal_url' exists
        """
        
        pass


    @abstractmethod
    async def close():
        """
        Close the connection to DB, etc.
        """
        
        pass