from datetime import timedelta
from pathlib import Path
from typing import TypedDict

from pydantic._internal._model_construction import ModelMetaclass

from panther.throttling import Throttling


class JWTConfig:
    def __init__(
            self,
            key: str,
            algorithm: str = 'HS256',
            life_time: timedelta | int = timedelta(days=1),
            refresh_life_time: timedelta | int = None,
    ):
        self.key = key
        self.algorithm = algorithm
        self.life_time = life_time
        if refresh_life_time:
            self.refresh_life_time = refresh_life_time
        else:
            self.refresh_life_time = self.life_time * 2


class Config(TypedDict):
    base_dir: Path
    monitoring: bool
    log_queries: bool
    default_cache_exp: timedelta | None
    throttling: Throttling | None
    secret_key: bytes | None
    middlewares: list
    reversed_middlewares: list
    user_model: ModelMetaclass | None
    authentication: ModelMetaclass | None
    jwt_config: JWTConfig | None
    models: list[dict]
    urls: dict
    db_engine: str
    websocket_connections: any  # type: WebsocketConnections


config: Config = {
    'base_dir': Path(),
    'monitoring': False,
    'log_queries': False,
    'default_cache_exp': None,
    'throttling': None,
    'secret_key': None,
    'middlewares': [],
    'reversed_middlewares': [],
    'user_model': None,
    'authentication': None,
    'jwt_config': None,
    'models': [],
    'urls': {},
    'db_engine': '',
    'websocket_connections': None,
}
