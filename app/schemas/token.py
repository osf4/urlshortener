from pydantic import BaseModel

class AccessToken(BaseModel):
    """
    Access token that is used to get access to the account
    """
    
    access_token: str
    type: str = 'bearer'