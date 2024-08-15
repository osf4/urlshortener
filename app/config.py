from dataclasses import dataclass
from datetime import timedelta
from dacite import from_dict, Config as DaciteConfig
from pytimeparse import parse

from yaml import load, CLoader as Loader


def _parse_expire_time(expire_time: str) -> timedelta:
    """
    Parse expiration time of access tokens from config file into timedelta
    """
    
    return timedelta(seconds = parse(expire_time))


@dataclass
class DatabaseConfig:
    """
    Settings to connect to the database
    """
    
    host: str
    port: int
    name: str


@dataclass
class JWTConfig:
    """
    Settings to use JWT tokens
    """
    
    secret_key: str
    algorithm: str
    access_token_expire_time: timedelta = timedelta(days = 5)


@dataclass
class Config:
    """
    Application config that is contained in 'config.yaml' file

    Example of the config file:

    database:
      host: 'localhost'
      port: 27017
      name: 'urlshortener'

    jwt:
      secret_key: '21a573afbd1a20db203fc268836e64304edd260eeb5bebc44f7bf012861703d8'
      algorithm: 'HS256'
      access_token_expire_time: '2d'
    """
    
    __dacite_config = DaciteConfig(type_hooks = {
        timedelta: _parse_expire_time,
    })


    database: DatabaseConfig
    jwt: JWTConfig


    @staticmethod
    def load(config_path = 'config.yaml') -> 'Config':
        with open(config_path) as config_file:
            config = load(config_file, Loader = Loader)

        return from_dict(Config, config, Config.__dacite_config)