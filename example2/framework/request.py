import orjson
from dataclasses import dataclass
from framework.logger import logger


@dataclass(frozen=True)
class Headers:
    accept_encoding: str
    content_length: int
    content_type: str
    user_agent: str
    connection: str
    accept: str
    host: str


class Request:
    def __init__(self, scope: dict, body):
        """
        :param data: should be dict or str
        """
        self.scope = scope
        self._body = body

    @property
    def headers(self):
        _headers = {}
        for header in self.scope['headers']:
            key, value = header
            _headers[key.decode('utf-8')] = value.decode('utf-8')
        return Headers(
            accept_encoding=_headers.get('accept-encoding'),
            content_length=_headers.get('content_length'),
            content_type=_headers.get('content-type'),
            user_agent=_headers.get('user-agent'),
            connection=_headers.get('connection'),
            accept=_headers.get('accept'),
            host=_headers.get('host')
        )

    @property
    def query_params(self):
        query_string = self.scope['query_string'].decode('utf-8').split('&')
        params = {}
        for param in query_string:
            k, *_, v = param.split('=')
            params[k] = v
        return params

    @property
    def method(self):
        return self.scope['method']

    @property
    def path(self):
        return self.scope['path']

    @property
    def server(self):
        return self.scope['server']

    @property
    def client(self):
        return self.scope['client']

    @property
    def http_version(self):
        return self.scope['http_version']

    @property
    def scheme(self):
        return self.scope['scheme']

    @property
    def data(self):
        body = self._body.decode('utf-8')
        if self.headers.content_type == 'application/json':
            _data = orjson.loads(body)
        elif self.headers.content_type.find('multipart/form-data') == 0:
            # TODO: Handle Multipart Form Data
            logger.error(f"We Don't Handle Multipart Request Yet.")
            _data = None
        else:
            logger.error(f'{self.headers.content_type} Is Not Supported.')
            _data = None
        return _data
