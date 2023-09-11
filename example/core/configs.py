"""Generated by Panther."""
from datetime import timedelta
from pathlib import Path

from panther.throttling import Throttling
from panther.utils import load_env

BASE_DIR = Path(__name__).resolve().parent
env = load_env(BASE_DIR / '.env')

# MONITORING = True

# LOG_QUERIES = True

# Load Env Variables
DB_NAME = env['DB_NAME']
DB_HOST = env['DB_HOST']
DB_PORT = env['DB_PORT']
SECRET_KEY = env['SECRET_KEY']
DB_USERNAME = env['DB_USERNAME']
DB_PASSWORD = env['DB_PASSWORD']

# # # More Info: https://pantherpy.github.io/middlewares/
MIDDLEWARES = [
    # TODO: change middleware
    # Go To https://framework.org/SupportedDatabase For More Options
    ('panther.middlewares.db.Middleware', {'url': f'pantherdb://{BASE_DIR}/{DB_NAME}.pdb'}),
    # ('panther.middlewares.db.Middleware', {'url': f'mongodb://{DB_HOST}:27017/{DB_NAME}'}),
    ('panther.middlewares.redis.Middleware', {'host': '127.0.0.1', 'port': 6379}),
]
"""
mongodb://[Username:Password(optional)]@HostName:Port/?aruguments
note: if your password has special characters, you would need to URL-Encode.

ex : mongodb://my-name:my-pass@localhost:27017/?authSource=users
"""
# # # More Info: Https://PantherPy.GitHub.io/authentications/
AUTHENTICATION = 'panther.authentications.JWTAuthentication'

# Only If Authentication Set To JWT
JWTConfig = {
    'algorithm': 'HS256',
    'life_time': timedelta(days=2),
    'key': SECRET_KEY,
}


URLs = 'core.urls.urls'

USER_MODEL = 'app.models.User'

DEFAULT_CACHE_EXP = timedelta(seconds=10)

# THROTTLING = Throttling(rate=10, duration=timedelta(seconds=10))
