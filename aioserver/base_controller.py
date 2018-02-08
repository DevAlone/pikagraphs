from bot.db import DB

import abc
import aiohttp
from aiohttp import web


class BaseController(abc.ABC):
    def __init__(self, base_url: str, app):
        self.db = DB.get_instance()
        self.db_pool = None
        self.app = app
        self.base_url = base_url

    @abc.abstractmethod
    async def get(self, request: aiohttp.ClientRequest):
        pass

    @abc.abstractmethod
    async def post(self, request: aiohttp.ClientRequest):
        pass

    def enable(self, allowed_methods: list=None):
        if allowed_methods is None:
            allowed_methods = ['GET', 'POST']

        for method in allowed_methods:
            {
                'GET': lambda: self.app.router.add_get(self.base_url, self._get),
                'POST': lambda: self.app.router.add_post(self.base_url, self._post),
            }[method]()

    def _prepare_params(self, params: dict) -> dict:
        return params

    async def _request(self, method: str, request: aiohttp.ClientRequest):
        if self.db_pool is None:
            self.db_pool = await self.db.get_pool()

        requested_method = {
            'GET': self.get,
            'POST': self.post,
        }[method]

        kwargs = dict(request.query)

        kwargs['request'] = request

        try:
            kwargs = self._prepare_params(kwargs)
        except ValueError as ex:
            return web.json_response({
                'status': 'error',
                'error_message': str(ex),
            })

        try:
            return web.json_response(
                await requested_method(**kwargs)
            )
        except NotAllowedException:
            return web.json_response({
                'status': 'error',
                'error_message': 'Not allowed',
            })

    async def _get(self, request: aiohttp.ClientRequest):
        return await self._request('GET', request)

    async def _post(self, request: aiohttp.ClientRequest):
        return await self._request('POST', request)

class NotAllowedException(BaseException):
    pass
