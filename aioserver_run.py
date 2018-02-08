from pikabot_graphs import settings
from restycorn.server import Server
from restycorn import postgresql
from restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource

if __name__ == '__main__':
    server = Server('0.0.0.0')
    server.set_base_address('/api')

    db = postgresql.get_instance(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME'],
    )

    server.register_resource('users', PostgreSQLReadOnlyResource(
        db=db,
        fields=('id', 'username', 'info', 'avatar_url', 'rating', 'comments_count', 'posts_count', 'hot_posts_count',
                'pluses_count', 'minuses_count', 'last_update_timestamp', 'subscribers_count', 'is_rating_ban',
                'updating_period', 'is_updated', 'pikabu_id', 'gender', 'approved', 'awards', 'signup_timestamp',),
        table_name='core_user',
        order_by=(
            'rating',
            'username',
            'subscribers_count',
            'comments_count',
            'posts_count',
            'hot_posts_count',
            'pluses_count',
            'minuses_count',
            'last_update_timestamp',
            'updating_period',
            'pikabu_id',
            'approved',
            'signup_timestamp',
            'id',
        ),
        search_by=('username', ),
    ))
    server.run()
# import functools
#
# import bot.init_django_models
# from aioserver.base_controller import NotAllowedException
# from aioserver.params_controller import ParamsController
# from aioserver.types import uint
# from bot.db import DB
# from bot.users_module import UsersModule
#
# import abc
# import inspect
# import asyncio
# import aiohttp
# from aiohttp import web
#
#
# async def index(request: aiohttp.ClientRequest):
#     return web.json_response({
#         'methods': {
#             'users': ['GET', ],
#             'communities': ['GET', ],
#         }
#     })
#
#
# def sql_record_to_dict(sql_record) -> dict:
#     result = {}
#     for key, val in sql_record.items():
#         result[key] = val
#
#     return result
#
#
# class UsersController(ParamsController):
#     def post(self, request):
#         raise NotAllowedException()
#
#     async def get(self, request, page: uint=0, order_by: str="", search: str="") -> dict:
#         async with self.db_pool.acquire() as connection:
#             # bindings = []
#             # sql_request = 'SELECT * FROM core_user '
#             #
#             # if search:
#             #     sql_request += "WHERE username LIKE '%${}".format(str(len(bindings))) + "::text%' "
#             #     bindings.append(search)
#             #
#             # if order_by:
#             #     sql_request += ' ORDER BY $' + str(len(bindings) + 1)
#             #     bindings.append(order_by)
#             #
#             # if page:
#             #     sql_request += ' OFFSET $' + str(len(bindings) + 1)
#             #     bindings.append(page * 50)
#             #
#             # sql_request += ' LIMIT 50;'
#
#             bindings = []
#             sql_request = '''
#                 SELECT * FROM core_user
#                 WHERE username LIKE '%adm%'
#                 ORDER BY -rating
#                 LIMIT 50'''
#
#             # print(sql_request)
#             # print(bindings)
#
#             user_list = await connection.fetch(sql_request, *bindings)
#             user_list = [sql_record_to_dict(sql_user) for sql_user in user_list]
#
#             return {
#                 'data': user_list
#             }
#
# def main():
#     app = web.Application()
#     app.router.add_get('/', index)
#
#     UsersController('/users', app).enable(['GET'])
#
#     web.run_app(app)
#
#
# if __name__ == '__main__':
#     main()
