import hashlib
from datetime import datetime, timedelta
from pathlib import Path

from panther.logger import logger


def load_env(env_file: str | Path, /) -> dict[str, str]:
    variables = dict()

    if env_file is None or not Path(env_file).is_file():
        logger.critical(f'"{env_file}" is not valid file for load_env()')
        return variables

    with open(env_file) as file:
        for line in file.readlines():
            line = line.strip()
            if not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                variables[key] = value
    return variables


def generate_secret_key() -> str:
    from cryptography.fernet import Fernet
    return Fernet.generate_key().decode()


def round_datetime(dt: datetime, delta: timedelta):
    return datetime.min + round((dt - datetime.min) / delta) * delta


def generate_hash_value_from_string(string_value: str) -> str:
    # The point of this method is for maintenance, if we want to change
    # the hash algorithm in the future, it will be easy.
    return hashlib.sha256(string_value.encode('utf-8')).hexdigest()
