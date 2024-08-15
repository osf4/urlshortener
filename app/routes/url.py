from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.url import UrlCreateIn, UrlCreateOut, UrlInfo
from app.unique_url import generate_url
from app.dependencies import CurrentUserDependency, StorageDependency


async def must_be_url_owner(internal_url: str | None, 
                            user: CurrentUserDependency,
                            storage: StorageDependency):
    """
    Raise HTTPException if the URL does not exist or the user is not the owner
    """
    
    if not internal_url:
        return

    if not await storage.url_exists(internal_url):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The URL "{internal_url}" was not found'
        )
    
    url_owner = await storage.get_url_owner(internal_url)
    if not url_owner == user.username:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'You are not the owner of the URL',
        )
    

router = APIRouter(
    prefix = '/url',
    tags = ['URL'],
    dependencies = [Depends(must_be_url_owner)]
)


@router.post('/')
async def create_url(current_user: CurrentUserDependency, 
                     new_url: UrlCreateIn,
                     storage: StorageDependency) -> UrlCreateOut:
    
    internal_url = generate_url()

    await storage.create_url(owner_username = current_user.username,
                             original_url = new_url.original_url,
                             internal_url = internal_url)
    
    return UrlCreateOut(original_url = new_url.original_url,
                        owner = current_user.username, 
                        active = True, 
                        internal_url = internal_url)


@router.get('/{internal_url}/info')
async def get_url(internal_url: str, 
                  storage: StorageDependency) -> UrlInfo:
    
    return await storage.get_url(internal_url)


@router.put('/{internal_url}')
async def change_url_active(internal_url: str, 
                            active: bool,
                            storage: StorageDependency) -> UrlInfo:
    
    if active:
        await storage.enable_url(internal_url)

    else:
        await storage.disable_url(internal_url)

    return await storage.get_url(internal_url)


@router.delete('/{internal_url}')
async def delete_url(internal_url: str,
                     storage: StorageDependency) -> UrlInfo:
    
    url = await storage.get_url(internal_url)
    await storage.delete_url(internal_url)

    return url
