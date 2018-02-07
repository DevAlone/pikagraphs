import functools

import bot.init_django_models
from bot.db import DB
from bot.users_module import UsersModule

import abc
import inspect
import asyncio
import aiohttp
from aiohttp import web


async def index(request: aiohttp.ClientRequest):
    return web.json_response({
        'methods': {
            'users': ['GET', ],
            'communities': ['GET', ],
        }
    })

class ParamsValidationError(BaseException):
    pass


class BaseView:
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
        except ParamsValidationError as ex:
            return web.json_response({
                'status': 'error',
                'error_message': str(ex),
            })

        return web.json_response(
            await requested_method(**kwargs)
        )

    async def _get(self, request: aiohttp.ClientRequest):
        return await self._request('GET', request)

    async def _post(self, request: aiohttp.ClientRequest):
        return await self._request('POST', request)


class ParamsView(BaseView):
    def _prepare_params(self, params: dict) -> dict:
        signature = inspect.signature(self.get)
        signature_params = signature.parameters

        for key, val in params.items():
            if key not in signature_params:
                raise ParamsValidationError('key "{}" is not allowed here'.format(key))

        for param_name, parameter_info in signature_params.items():
            if param_name not in params and parameter_info.default is inspect.Parameter.empty:
                raise ParamsValidationError('param "{}" is required'.format(param_name))

        try:
            bind = signature.bind(**params)
        except TypeError:
            raise ParamsValidationError('Not enough params')

        bind.apply_defaults()

        result = bind.arguments

        for key, parameter_info in signature_params.items():
            if key in result:
                if parameter_info.annotation is inspect.Parameter.empty \
                        or (parameter_info.default is None and result[key] is None):
                    continue

                if type(result[key]) is not parameter_info.annotation:
                    try:
                        result[key] = parameter_info.annotation(result[key])
                    except ValueError:
                        raise ParamsValidationError('key "{}" should be "{}" or type convertable to "{}"'.format(
                            key, parameter_info.annotation, parameter_info.annotation))



        return result


def sql_record_to_dict(sql_record) -> dict:
    result = {}
    for key, val in sql_record.items():
        result[key] = val

    return result


class UsersView(ParamsView):
    async def get(self, request, page: int=0, order_by: str="") -> dict:
        async with self.db_pool.acquire() as connection:
            bindings = []
            sql_request = 'SELECT * FROM core_user '
            if order_by:
                sql_request += ' ORDER BY $' + str(len(bindings) + 1)
                bindings.append(order_by)

            if page < 0:
                # TODO: refactor
                raise ParamsValidationError("page should be positive")

            if page:
                sql_request += ' OFFSET $' + str(len(bindings) + 1)
                bindings.append(page * 10)

            sql_request += ' LIMIT 10;'

            print(sql_request)
            print(bindings)

            user_list = await connection.fetch(sql_request, *bindings)
            user_list = [sql_record_to_dict(sql_user) for sql_user in user_list]

            return {
                'data': user_list
            }

#
# def strict_types(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         signature = inspect.signature(func)
#         parameters = signature.parameters
#         print([(key, val.annotation) for key, val in parameters.items()])
#
#         bind = signature.bind(*args, **kwargs)
#
#         bind.apply_defaults()
#         kwargs = bind.arguments
#
#         for key, val in parameters.items():
#             if key in kwargs:
#                 if val.annotation is inspect.Parameter.empty or (val.default is None and kwargs[key] is None):
#                     continue
#
#                 if type(kwargs[key]) is not val.annotation:
#                     try:
#                         kwargs[key] = val.annotation(kwargs[key])
#                     except ValueError:
#                         raise ParamsValidationError(
#                             'Type of param "{}" doesn\'t match to signature or is not convertable to signature '
#                             'type'.format(
#                             key
#                         ))
#
#         return func(**kwargs)
#
#     return wrapper
#
# @strict_types
# def test(param1, param2: int=None, param3: str="def value"):
#     print('test works')
#     print(type(param1))
#     print(param1)
#     print(type(param2))
#     print(param2)
#     print(type(param3))
#     print(param3)


def main():
    app = web.Application()
    app.router.add_get('/', index)

    UsersView('/users', app).enable(['GET'])

    web.run_app(app)


if __name__ == '__main__':
    main()
