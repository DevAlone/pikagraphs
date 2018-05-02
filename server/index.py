import asyncio
import asyncpgsa
from asyncpgsa.pgsingleton import NotInitializedError

from restycorn.restycorn.exceptions import MethodIsNotAllowedException
from restycorn.restycorn.postgresql_serializer import PostgreSQLSerializer
from restycorn.restycorn.read_only_resource import ReadOnlyResource
from restycorn.restycorn.restycorn_types import uint


class Index(ReadOnlyResource):
    time_cached = True
    time_cache_seconds = 60

    async def list(self) -> list:
        raise MethodIsNotAllowedException()

    async def get(self, item_id) -> object:
        if item_id == 'counters':
            number_of_users = int((await asyncpgsa.pg.fetchrow('''
                SELECT COUNT(*) FROM core_pikabuuser
            '''))[0])
            number_of_updated_users = int((await asyncpgsa.pg.fetchrow('''
                SELECT COUNT(*) FROM core_user
                WHERE is_updated = true
            '''))[0])

            return {
                'number_of_users': number_of_users,
                'number_of_updated_users': number_of_updated_users,
            }

        raise MethodIsNotAllowedException()


class UserDistributions(ReadOnlyResource):
    def __init__(self):
        self.storage = {}
        self.fields = {
            'rating': {'window_size': 5000},
            'comments_count': {'window_size': 1000},
            'posts_count': {'window_size': 1000},
            'hot_posts_count': {'window_size': 1000},
            'pluses_count': {'window_size': 1000},
            'minuses_count': {'window_size': 1000},
            'subscribers_count': {'window_size': 1000},
            'updating_period': {'window_size': 1000},
            'signup_timestamp': {'window_size': 86400},
            'last_update_timestamp': {'window_size': 1000},
            # 'gender',
        }
        # asyncio.get_event_loop()
        asyncio.ensure_future(self.updater_loop())

    async def list(self) -> list:
        raise MethodIsNotAllowedException()

    async def get(self, item_id: str) -> object:
        # table_name = 'core_user'
        field_name = item_id
        if field_name not in self.fields:
            raise MethodIsNotAllowedException()

        try:
            return self.storage[field_name]
        except KeyError:
            self.storage[field_name] = await self.make_distribution(
                'core_user',
                field_name,
                self.fields[field_name]['window_size']
            )
            return self.storage[field_name]

    async def updater_loop(self):
        while True:
            try:
                await self.update_storage()
                await asyncio.sleep(10 * 60)
            except NotInitializedError:
                await asyncio.sleep(10)

    async def update_storage(self):
        print('start updating')
        for field_name, value in self.fields.items():
            window_size = value['window_size']
            self.storage[field_name] = await self.make_distribution('core_user', field_name, window_size)

    async def make_distribution(self, table_name, field_name, window_size):
        sql_arguments = []
        if field_name == 'signup_timestamp':
            sql_request = '''
            WITH stats AS (
                SELECT MIN(signup_timestamp) as min_value, MAX(signup_timestamp) as max_value
                FROM core_user
            )
            SELECT 
                width_bucket(signup_timestamp, min_value, max_value, (max_value - min_value) / ($1)) as bucket,
                MIN(signup_timestamp) as x,
                COUNT(*) AS y
            FROM 
                core_user, stats
            GROUP BY
                bucket
            ORDER BY
                bucket;'''

            sql_arguments.append(window_size)
        else:
            sql_request = '''
                WITH stats AS (
                    SELECT MIN(:field_name) as min_value, MAX(:field_name) as max_value
                    FROM :table_name
                )
                SELECT 
                    width_bucket(:field_name, min_value, max_value, :window_size) as bucket,
                    -- int4range(MIN(:field_name), MAX(:field_name), '[]') as x,
                    MIN(:field_name) as x,
                    COUNT(*) AS y
                FROM 
                    :table_name, stats
                GROUP BY
                    bucket
                ORDER BY
                    bucket;
            '''.replace(':field_name', field_name)\
                .replace(':table_name', table_name)\
                .replace(':window_size', str(window_size))

        items = await asyncpgsa.pg.fetch(sql_request, *sql_arguments)

        return [PostgreSQLSerializer(['x', 'y']).serialize(item) for item in items if item['y'] != 0]


class CommentsDistributions(ReadOnlyResource):
    def __init__(self):
        self.storage = {}
        self.fields = {
            'creation_timestamp': {'window_size': 86400},
            # 'rating': {'window_size': 5000},
            # 'comments_count': {'window_size': 1000},
            # 'posts_count': {'window_size': 1000},
            # 'hot_posts_count': {'window_size': 1000},
            # 'pluses_count': {'window_size': 1000},
            # 'minuses_count': {'window_size': 1000},
            # 'subscribers_count': {'window_size': 1000},
            # 'updating_period': {'window_size': 1000},
            # 'signup_timestamp': {'window_size': 86400},
            # 'last_update_timestamp': {'window_size': 1000},
            # 'gender',
        }
        # asyncio.get_event_loop()
        # asyncio.ensure_future(self.updater_loop())

    async def list(self) -> list:
        raise MethodIsNotAllowedException()

    async def get(self, item_id: str, window_size: uint) -> object:
        # table_name = 'core_user'
        field_name = item_id
        if field_name not in self.fields or window_size < 60:
            raise MethodIsNotAllowedException()

        return await self.make_distribution(
            'comments',
            field_name,
            window_size,
        )

    async def update_storage(self):
        print('start updating')
        for field_name, value in self.fields.items():
            window_size = value['window_size']
            self.storage[field_name] = await self.make_distribution('core_user', field_name, window_size)

    async def make_distribution(self, table_name, field_name, window_size):
        sql_arguments = []
        if field_name == 'creation_timestamp':
            _sql_request = '''
            WITH stats AS (
                SELECT MIN(signup_timestamp) as min_value, MAX(signup_timestamp) as max_value
                FROM core_user
            )
            SELECT 
                width_bucket(signup_timestamp, min_value, max_value, (max_value - min_value) / ($1)) as bucket,
                MIN(signup_timestamp) as x,
                COUNT(*) AS y
            FROM 
                core_user, stats
            GROUP BY
                bucket
            ORDER BY
                bucket;'''
            sql_request = '''
            WITH stats AS (
                SELECT MIN(creation_timestamp) as min_value, MAX(creation_timestamp) as max_value
                FROM comments WHERE creation_timestamp >= $2
            ), number_of_bars_table AS (
                SELECT (stats.max_value - stats.min_value) / ($1) as number_of_bars FROM stats
            )
            SELECT 
                width_bucket(
                    creation_timestamp, 
                    min_value, 
                    max_value, 
                    (CASE WHEN (number_of_bars > 0) THEN number_of_bars ELSE 1 END)
                ) as bucket,
                MIN(creation_timestamp) as x,
                COUNT(*) AS y
            FROM 
                comments, stats, number_of_bars_table
            WHERE comments.creation_timestamp >= $2
            GROUP BY
                bucket
            ORDER BY
                bucket;
            '''

            sql_arguments.append(window_size)
            sql_arguments.append(0)
        else:
            raise MethodIsNotAllowedException()
            # sql_request = '''
            # WITH stats AS (
            #     SELECT MIN(:field_name) as min_value, MAX(:field_name) as max_value
            #     FROM :table_name WHERE :field_name >= $2
            # ), number_of_bars_table AS (
            #     SELECT (stats.max_value - stats.min_value) / ($1) as number_of_bars FROM stats
            # )
            # SELECT
            #     width_bucket(
            #         :field_name,
            #         min_value,
            #         max_value,
            #         $1
            #     ) as bucket,
            #     MIN(:field_name) as x,
            #     COUNT(*) AS y
            # FROM
            #     :table_name, stats, number_of_bars_table
            # WHERE comments.:field_name >= $2
            # GROUP BY
            #     bucket
            # ORDER BY
            #     bucket;
            # '''.replace(':field_name', field_name)\
            #     .replace(':table_name', table_name)
            # sql_arguments.append(window_size)
            # sql_arguments.append(0)

        items = await asyncpgsa.pg.fetch(sql_request, *sql_arguments)

        return [PostgreSQLSerializer(['x', 'y']).serialize(item) for item in items if item['y'] != 0]


index = Index()
user_distributions = UserDistributions()
comment_distributions = CommentsDistributions()
