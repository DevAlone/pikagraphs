import asyncio
import logging

import asyncpgsa
import sqlalchemy

import models
from pikabot_graphs import settings
from restycorn.restycorn.base_resource import BaseResource
from restycorn.restycorn.postgresql import db
from restycorn.restycorn.postgresql_serializer import PostgreSQLSerializer
from restycorn.restycorn.restycorn_types import uint
from restycorn.restycorn.server import Server
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource


class Scoreboards(BaseResource):
    def __init__(self, scoreboardentry_table, scoreentry_table):
        self.scoreboardentry_table = scoreboardentry_table
        self.scoreentry_table = scoreentry_table

    async def list(self, page: uint=0) -> list:
        sql_request = self.scoreboardentry_table.select().order_by(
            self.scoreboardentry_table.c.parse_timestamp.desc()).limit(50)

        if page:
            sql_request = sql_request.offset(page * 50)

        items = await asyncpgsa.pg.fetch(sql_request)

        result = [PostgreSQLSerializer(('id', 'parse_timestamp')).serialize(item) for item in items]

        for i in range(len(result)):
            sql_request = sqlalchemy.select(['*']).select_from(self.scoreentry_table).where(
                self.scoreentry_table.c.scoreboard_entry_id == result[i]['id']
            )

            print(str(sql_request))
            print(str(sql_request.compile().params))

            score_entries = [
                PostgreSQLSerializer(
                    ('username', 'avatar_url', 'score', 'date', )
                ).serialize(item)
                for item in (await asyncpgsa.pg.fetch(sql_request))
            ]

            result[i]['score_entries'] = score_entries

        return result


async def main():
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

    server.register_resource('users', PostgreSQLReadOnlyResource(
        sqlalchemy_table=models.core_user,
        fields=('id', 'username', 'info', 'avatar_url', 'rating', 'comments_count', 'posts_count', 'hot_posts_count',
                'pluses_count', 'minuses_count', 'last_update_timestamp', 'subscribers_count', 'is_rating_ban',
                'updating_period', 'is_updated', 'pikabu_id', 'gender', 'approved', 'awards', 'signup_timestamp',
                'deleted'),
        id_field='username',
        order_by=('id', 'rating', 'username', 'subscribers_count', 'comments_count', 'posts_count',
                  'hot_posts_count', 'pluses_count', 'minuses_count', 'last_update_timestamp', 'updating_period',
                  'pikabu_id', 'approved', 'signup_timestamp',),
        search_by=('username', 'info',),
        filter_by={
            'username': ('=',),
            'rating': ('=', '>', '<'),
            'deleted': ('=', ),
        },
        page_size=50,
    ))

    server.register_resource('pikabu_users', PostgreSQLReadOnlyResource(
        sqlalchemy_table=models.core_pikabuuser,
        fields=('pikabu_id', 'username', 'is_processed' ),
        id_field='pikabu_id',
        order_by=('pikabu_id', 'username', ),
        search_by=('username', ),
        filter_by={
            'pikabu_id': ('=', '>', '<'),
            'username': ('=', ),
            'is_processed': ('=',),
        },
        page_size=50,
    ))

    server.register_resource('communities', PostgreSQLReadOnlyResource(
        sqlalchemy_table=models.communities_app_community,
        fields=('id', 'url_name', 'name', 'description', 'avatar_url', 'background_image_url', 'subscribers_count',
                'stories_count', 'last_update_timestamp'),
        id_field='url_name',
        order_by=('id', 'subscribers_count', 'name', 'stories_count', 'last_update_timestamp', ),
        search_by=('url_name', 'name', 'description',),
        page_size=50,
    ))

    def register_user_graph_item_resource(resource_name, sqlalchemy_table):
        server.register_resource(resource_name, PostgreSQLReadOnlyResource(
            sqlalchemy_table=sqlalchemy_table,
            fields=('timestamp', 'value',),
            id_field='id',
            order_by=('id',),
            filter_by={
                'user_id': ('=',),
            },
            paginated=False,
        ))

    register_user_graph_item_resource('graph/user/rating', models.core_userratingentry)
    register_user_graph_item_resource('graph/user/subscribers', models.core_usersubscriberscountentry)
    register_user_graph_item_resource('graph/user/comments', models.core_usercommentscountentry)
    register_user_graph_item_resource('graph/user/posts', models.core_userpostscountentry)
    register_user_graph_item_resource('graph/user/hot_posts', models.core_userhotpostscountentry)
    register_user_graph_item_resource('graph/user/pluses', models.core_userplusescountentry)
    register_user_graph_item_resource('graph/user/minuses', models.core_userminusescountentry)

    def register_community_graph_item_resource(resource_name):
        server.register_resource('graph/community/' + resource_name, PostgreSQLReadOnlyResource(
            sqlalchemy_table=models.communities_app_communitycountersentry,
            fields=('timestamp', '{} as value'.format(resource_name)),
            id_field='community_id',
            order_by=('id',),
            filter_by={
                'community_id': ('=',),
            },
            paginated=False,
        ))

    register_community_graph_item_resource('subscribers_count')
    register_community_graph_item_resource('stories_count')

    # scoreboards
    # new_year_2018_game/scoreboards
    # new_year_2018_game/scoreboards
    # server.register_resource('new_year_2018_game/scoreboards', PostgreSQLReadOnlyResource(
    #     sqlalchemy_table=models.pikabu_new_year_18_game_app_scoreboardentry,
    #     fields=('id', 'parse_timestamp',),
    #     id_field='id',
    #     order_by=('parse_timestamp', 'id',),
    #     page_size=50,
    # ))

    server.register_resource('new_year_2018_game/top_items', PostgreSQLReadOnlyResource(
        sqlalchemy_table=models.pikabu_new_year_18_game_app_topitem,
        fields=('username', 'avatar_url', 'score', 'date',),
        id_field='score_entry_id',
        order_by=('score_entry_id',),
        page_size=50,
        join=(
            models.pikabu_new_year_18_game_app_scoreentry,
            models.pikabu_new_year_18_game_app_topitem.c.score_entry_id ==
            models.pikabu_new_year_18_game_app_scoreentry.c.scoreboard_entry_id
        )
    ))

    server.register_resource(
        'new_year_2018_game/scoreboards',
        Scoreboards(models.pikabu_new_year_18_game_app_scoreboardentry, models.pikabu_new_year_18_game_app_scoreentry)
    )

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
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main()).run()
