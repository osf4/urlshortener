from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.dependencies import StorageDependency


router = APIRouter()


async def url_must_be_active(internal_url: str, 
                             storage: StorageDependency):
    
    url = await storage.get_url(internal_url)
    if not url.active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'The URL is not active!'
        )
    

@router.get('/{internal_url}', dependencies = [Depends(url_must_be_active)])
async def get_redirect(internal_url: str, storage: StorageDependency):
    if not await storage.url_exists(internal_url):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'The page was not found!',
        )
    
    redirect_url = await storage.get_original_url(internal_url)
    return RedirectResponse(url = redirect_url)


@router.get('/')
async def get_empty_redirect():
    return RedirectResponse(url = 'https://google.com')