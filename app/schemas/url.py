from pydantic import BaseModel


class UrlBase(BaseModel):
    """
    Base model for all URLs
    """
    
    original_url: str


class UrlInfo(UrlBase):
    """
    Represent the full information about the URL
    """

    owner: str
    active: bool
    internal_url: str


class UrlCreateIn(UrlBase):
    """
    Represent URL creation request
    """
    
    pass


class UrlCreateOut(UrlInfo):
    """
    Represent URL creation response
    """
    
    pass