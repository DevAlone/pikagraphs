import asyncpgsa
import sqlalchemy

import models
from restycorn.restycorn.exceptions import MethodIsNotAllowedException
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource
from restycorn.restycorn.postgresql_serializer import PostgreSQLSerializer
from restycorn.restycorn.read_only_resource import ReadOnlyResource
from restycorn.restycorn.restycorn_types import uint


class Scoreboards(ReadOnlyResource):
    def get(self, item_id) -> object:
        raise MethodIsNotAllowedException()

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


scoreboards = Scoreboards(
    models.pikabu_new_year_18_game_app_scoreboardentry,
    models.pikabu_new_year_18_game_app_scoreentry
)


top_items = PostgreSQLReadOnlyResource(
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
)
