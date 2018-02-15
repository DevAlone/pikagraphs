import models
from pikabot_graphs import settings
from restycorn.restycorn.server import Server
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource

import asyncio
import logging
import asyncpgsa

from server.communities import communities, get_community_graph_item_resource
from server.index import index, user_distributions
from server.pikabu_new_year_18_game import top_items, scoreboards
from server.users import pikabu_users, users, get_user_graph_item_resource


async def create_server():
    await asyncpgsa.pg.init(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME'],
        min_size=5,
        max_size=100,
    )

    server = Server(
        '127.0.0.1',
        access_log_format='%Tfs %a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"')
    server.set_base_address('/api')

    server.register_resource('index', index)
    server.register_resource('graph/distribution/user', user_distributions)
    server.register_resource('users', users)
    server.register_resource('pikabu_users', pikabu_users)
    server.register_resource('communities', communities)

    server.register_resource('graph/user/rating', get_user_graph_item_resource(models.core_userratingentry))
    server.register_resource('graph/user/subscribers',
                             get_user_graph_item_resource(models.core_usersubscriberscountentry))
    server.register_resource('graph/user/comments', get_user_graph_item_resource(models.core_usercommentscountentry))
    server.register_resource('graph/user/posts', get_user_graph_item_resource(models.core_userpostscountentry))
    server.register_resource('graph/user/hot_posts', get_user_graph_item_resource(models.core_userhotpostscountentry))
    server.register_resource('graph/user/pluses', get_user_graph_item_resource(models.core_userplusescountentry))
    server.register_resource('graph/user/minuses', get_user_graph_item_resource(models.core_userminusescountentry))

    server.register_resource('graph/community/subscribers_count',
                             get_community_graph_item_resource('subscribers_count'))
    server.register_resource('graph/community/stories_count', get_community_graph_item_resource('stories_count'))

    server.register_resource('new_year_2018_game/top_items', top_items)
    server.register_resource('new_year_2018_game/scoreboards', scoreboards)

    # logging
    logger = logging.getLogger('aiohttp.access')

    logger.setLevel(logging.DEBUG)

    error_file_handler = logging.FileHandler('logs/{}.error.log'.format('aiohttp.access'))
    error_file_handler.setLevel(logging.ERROR)
    info_file_handler = logging.FileHandler('logs/{}.log'.format('aiohttp.access'))
    info_file_handler.setLevel(logging.INFO)

    logger.addHandler(error_file_handler)
    logger.addHandler(info_file_handler)

    if settings.DEBUG:
        debug_file_handler = logging.FileHandler('logs/{}.debug.log'.format('aiohttp.access'))
        debug_file_handler.setLevel(logging.DEBUG)
        logger.addHandler(debug_file_handler)

    return server


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_server()).run()
