from abc import ABC
from dataclasses import dataclass, asdict, field
from typing import Any
from dacite import from_dict, Config as DaciteConfig


class DatabaseModel(ABC):
    """
    Base class for all database models
    """
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


    @classmethod
    def from_dict(cls, 
                  dict: dict[str, Any], 
                  config: DaciteConfig | None = None) -> 'DatabaseModel':
        
        if dict is None:
            return None
        
        return from_dict(cls, dict, config)


@dataclass(kw_only = True)
class User(DatabaseModel):
    username: str
    hashed_password: str

    owned_urls: list[str] = field(default_factory = list)


@dataclass(kw_only = True)
class Url(DatabaseModel):
    original_url: str
    internal_url: str

    owner: str
    active: bool = True
