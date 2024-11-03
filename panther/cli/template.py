from datetime import datetime

from panther import version
from panther.utils import generate_secret_key

apis_py = """from datetime import datetime

from app.throttling import InfoThrottling

from panther import status, version
from panther.app import API
from panther.request import Request
from panther.response import Response
from panther.utils import timezone_now


@API()
async def hello_world_api():
    return {'detail': 'Hello World'}


@API(cache=True, throttling=InfoThrottling)
async def info_api(request: Request):
    data = {
        'panther_version': version(),
        'method': request.method,
        'query_params': request.query_params,
        'datetime_now': timezone_now().isoformat(),
        'user_agent': request.headers.user_agent,
    }
    return Response(data=data, status_code=status.HTTP_202_ACCEPTED)
"""

models_py = """from panther.db import Model
"""

serializers_py = """from panther.serializer import ModelSerializer
"""

throttling_py = """from datetime import timedelta

from panther.throttling import Throttling

InfoThrottling = Throttling(rate=5, duration=timedelta(minutes=1))
"""

app_urls_py = """from app.apis import hello_world_api, info_api

urls = {
    '/': hello_world_api,
    'info/': info_api,
}
"""

configs_py = """\"""
{PROJECT_NAME} Project (Generated by Panther on %s)
\"""

from pathlib import Path

from panther.utils import load_env

BASE_DIR = Path(__name__).resolve().parent
env = load_env(BASE_DIR / '.env')

SECRET_KEY = env['SECRET_KEY']{DATABASE}{REDIS}{VALKEY}{USER_MODEL}{AUTHENTICATION}{MONITORING}{LOG_QUERIES}{AUTO_REFORMAT}

# More Info: https://PantherPy.GitHub.io/urls/
URLs = 'core.urls.url_routing'

TIMEZONE = 'UTC'
""" % datetime.now().date().isoformat()

env = """SECRET_KEY='%s'
""" % generate_secret_key()

main_py = """from panther import Panther

app = Panther(__name__)
"""

urls_py = """from app.urls import urls as app_urls

url_routing = {
    '/': app_urls,
}
"""

git_ignore = """__pycache__/
.venv/
.idea/
logs/

.env
*.pdb
"""

requirements = """panther==%s
""" % version()

TEMPLATE = {
    'app': {
        '__init__.py': '',
        'apis.py': apis_py,
        'models.py': models_py,
        'serializers.py': serializers_py,
        'throttling.py': throttling_py,
        'urls.py': app_urls_py,
    },
    'core': {
        '__init__.py': '',
        'configs.py': configs_py,
        'urls.py': urls_py,
    },
    'main.py': main_py,
    '.env': env,
    '.gitignore': git_ignore,
    'requirements.txt': requirements,
}

single_main_py = """\"""
{PROJECT_NAME} Project (Generated by Panther on %s)
\"""
from datetime import datetime, timedelta
from pathlib import Path

from panther import Panther, status, version
from panther.app import API
from panther.request import Request
from panther.response import Response
from panther.throttling import Throttling
from panther.utils import load_env, timezone_now

BASE_DIR = Path(__name__).resolve().parent
env = load_env(BASE_DIR / '.env')

SECRET_KEY = env['SECRET_KEY']{DATABASE}{REDIS}{VALKEY}{USER_MODEL}{AUTHENTICATION}{MONITORING}{LOG_QUERIES}{AUTO_REFORMAT}

InfoThrottling = Throttling(rate=5, duration=timedelta(minutes=1))

TIMEZONE = 'UTC'


@API()
async def hello_world_api():
    return {'detail': 'Hello World'}


@API(cache=True, throttling=InfoThrottling)
async def info_api(request: Request):
    data = {
        'panther_version': version(),
        'method': request.method,
        'query_params': request.query_params,
        'datetime_now': timezone_now().isoformat(),
        'user_agent': request.headers.user_agent,
    }
    return Response(data=data, status_code=status.HTTP_202_ACCEPTED)


url_routing = {
    '/': hello_world_api,
    'info/': info_api,
}

app = Panther(__name__, configs=__name__, urls=url_routing)
""" % datetime.now().date().isoformat()

SINGLE_FILE_TEMPLATE = {
    'main.py': single_main_py,
    '.env': env,
    '.gitignore': git_ignore,
    'requirements.txt': requirements,
}

DATABASE_PANTHERDB_PART = """

# More Info: https://PantherPy.GitHub.io/database/
DATABASE = {
    'engine': {
        'class': 'panther.db.connections.PantherDBConnection',
        'path': BASE_DIR / 'database.{PANTHERDB_EXTENSION}',
        'encryption': {PANTHERDB_ENCRYPTION}
    }
}"""

DATABASE_MONGODB_PART = """

# More Info: https://PantherPy.GitHub.io/database/
DATABASE = {
    'engine': {
        'class': 'panther.db.connections.MongoDBConnection',
        'host': '127.0.0.1',
        'port': 27017,
        'database': '{PROJECT_NAME}'
    }
}"""

REDIS_PART = """

# More Info: https://PantherPy.GitHub.io/redis/
REDIS = {
    'class': 'panther.db.connections.RedisConnection',
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
}"""

VALKEY_PART = """

# More Info: https://PantherPy.GitHub.io/valkey/
VALKEY = {
    'class': 'panther.db.connections.ValkeyConnection',
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
}"""

USER_MODEL_PART = """

# More Info: https://PantherPy.GitHub.io/configs/#user_model
USER_MODEL = 'panther.db.models.BaseUser'"""

AUTHENTICATION_PART = """

# More Info: https://PantherPy.GitHub.io/authentications/
AUTHENTICATION = 'panther.authentications.JWTAuthentication'"""

MONITORING_PART = """

# More Info: https://PantherPy.GitHub.io/monitoring/
MONITORING = True"""

LOG_QUERIES_PART = """

# More Info: https://PantherPy.GitHub.io/log_queries/
LOG_QUERIES = True"""

AUTO_REFORMAT_PART = """

# More Info: https://pantherpy.github.io/configs/#auto_reformat/
AUTO_REFORMAT = True"""
