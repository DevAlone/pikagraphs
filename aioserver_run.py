import functools

import bot.init_django_models
from aioserver.base_controller import NotAllowedException
from aioserver.params_controller import ParamsController
from aioserver.types import uint
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


def sql_record_to_dict(sql_record) -> dict:
    result = {}
    for key, val in sql_record.items():
        result[key] = val

    return result


class UsersController(ParamsController):
    def post(self, request):
        raise NotAllowedException()

    async def get(self, request, page: uint=0, order_by: str="", search: str="") -> dict:
        async with self.db_pool.acquire() as connection:
            # bindings = []
            # sql_request = 'SELECT * FROM core_user '
            #
            # if search:
            #     sql_request += "WHERE username LIKE '%${}".format(str(len(bindings))) + "::text%' "
            #     bindings.append(search)
            #
            # if order_by:
            #     sql_request += ' ORDER BY $' + str(len(bindings) + 1)
            #     bindings.append(order_by)
            #
            # if page:
            #     sql_request += ' OFFSET $' + str(len(bindings) + 1)
            #     bindings.append(page * 50)
            #
            # sql_request += ' LIMIT 50;'

            bindings = []
            sql_request = '''
                SELECT * FROM core_user 
                WHERE username LIKE '%adm%' 
                ORDER BY -rating
                LIMIT 50'''

            # print(sql_request)
            # print(bindings)

            user_list = await connection.fetch(sql_request, *bindings)
            user_list = [sql_record_to_dict(sql_user) for sql_user in user_list]

            return {
                'data': user_list
            }

def main():
    app = web.Application()
    app.router.add_get('/', index)

    UsersController('/users', app).enable(['GET'])

    web.run_app(app)


if __name__ == '__main__':
    main()
