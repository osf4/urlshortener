from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from .base_storage import BaseStorage
from .models import User, Url

from .exceptions import UserExistsError, UrlExistsError, UserNotExistError, UrlNotExistError

class MongoStorage(BaseStorage):
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port

        self.__client = AsyncIOMotorClient(host, port)
        self.__database = self.__client[database]

        self.__users = self.__database['users']
        self.__urls = self.__database['urls']


    async def create_user(self, user: User):
        if await self.user_exists(user.username):
            raise UserExistsError(f'User {user.username} already exists')
        
        await self.__users.insert_one(user.to_dict())

    
    async def get_user(self, username: str) -> User | None:
        user_dict = await self.__users.find_one({'username': username})
        return User.from_dict(user_dict)
    

    async def delete_user(self, username: str):
        await self.__raise_if_user_not_exist(username)

        await self.__users.delete_one({'username': username})
        await self.__urls.delete_many({'owner': username})


    async def user_exists(self, username: str) -> bool:
        documents_count = await self.__users.count_documents({'username': username})
        return not documents_count == 0
    

    async def create_url(self,
                         *, 
                         owner_username: str, 
                         original_url: str, 
                         internal_url: str):

        await self.__raise_if_user_not_exist(owner_username)
        
        if await self.url_exists(internal_url):
            raise UrlExistsError(f'URL "{internal_url}" already exists')
        
        new_url = Url(original_url = original_url,
                      internal_url = internal_url,
                      owner = owner_username)
        
        await self.__urls.insert_one(new_url.to_dict())
        await self.__append_owned_urls(owner_username, internal_url)


    async def get_url(self, internal_url: str) -> Url | None:
        url_dict = await self.__urls.find_one({'internal_url': internal_url})
        return Url.from_dict(url_dict)
    

    async def get_url_owner(self, internal_url: str) -> str:
        await self.__raise_if_url_not_exist(internal_url)

        return await self.__extract_field(self.__urls,
                                          'owner',
                                          {'internal_url': internal_url})
    

    async def get_original_url(self, internal_url: str) -> str:
        await self.__raise_if_url_not_exist(internal_url)

        return await self.__extract_field(self.__urls,
                                          'original_url',
                                          {'internal_url': internal_url})

    
    async def enable_url(self, internal_url: str):
        await self.__set_url_active(internal_url, True)

    
    async def disable_url(self, internal_url: str):
        await self.__set_url_active(internal_url, False)

    
    async def delete_url(self, internal_url: str):
        await self.__raise_if_url_not_exist(internal_url)

        deleted_url = await self.__urls.find_one_and_delete({'internal_url': internal_url})
        await self.__remove_owned_url(deleted_url['owner'], internal_url)


    async def url_exists(self, internal_url: str) -> bool:
        documents_count = await self.__urls.count_documents({'internal_url': internal_url})
        return not documents_count == 0


    async def close(self):
        self.__client.close()

    
    async def __raise_if_user_not_exist(self, username: str):
        if not await self.user_exists(username):
            raise UserNotExistError(f'User {username} does not exist')
        
    
    async def __raise_if_url_not_exist(self, internal_url: str):
        if not await self.url_exists(internal_url):
            raise UrlNotExistError(f'URL "{internal_url}" does not exist')


    async def __append_owned_urls(self, username: str, internal_url: str):
        await self.__raise_if_user_not_exist(username)

        await self.__users.update_one({'username': username}, 
                                      {'$push': {'owned_urls': internal_url}})
        
    
    async def __remove_owned_url(self, username: str, internal_str: str):
        await self.__raise_if_user_not_exist(username)

        await self.__users.update_one({'username': username}, 
                                      {'$pull': {'owned_urls': internal_str}})
        

    async def __set_url_active(self, internal_url: str, active: bool):
        await self.__raise_if_url_not_exist(internal_url)

        await self.__urls.update_one({'internal_url': internal_url},
                                     {'$set': {'active': active}})
        
        
    async def __extract_field(self, 
                                  collection: AsyncIOMotorCollection,
                                  searched_field: str,
                                  condition: dict[str, Any]) -> Any:
        
        selected_field = await collection.find_one(condition, 
                                                   {searched_field: 1, '_id': 0})
        
        return selected_field[searched_field]
