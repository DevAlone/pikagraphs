from .base_resource import BaseResource
from .exceptions import MethodIsNotAllowedException, ParamsValidationException
from .postgresql import SQLRequestConstructor
from .postgresql_serializer import PostgreSQLSerializer
from .restycorn_types import uint


class PostgreSQLReadOnlyResource(BaseResource):
    def __init__(self, db, table_name, fields, order_by, search_by):
        self.db = db
        self.pool = None
        self.table_name = table_name
        self.fields = fields
        self.order_by_fields = order_by
        self.search_by_fields = search_by
        self.serializer = PostgreSQLSerializer(self.fields)
        self.page_size = 10

    async def init_pool(self):
        if self.pool is None:
            self.pool = await self.db.get_pool()

    async def list(self, page: uint=0, order_by: str=None, search_text: str=None) -> list:
        await self.init_pool()

        if order_by is None:
            order_by = self.order_by_fields[0]

        order_by = order_by.strip()

        if (order_by[1:] if order_by.startswith('-') else order_by) not in self.order_by_fields:
            raise ParamsValidationException("It's not allowed to sort by this field")

        sql_request = SQLRequestConstructor()\
            .select(self.fields)\
            .from_table(self.table_name)\

        if search_text:
            sql_request = sql_request.where().search_by(self.search_by_fields, search_text)

        sql_request = sql_request.order_by(order_by).limit(self.page_size)
        if page:
            sql_request = sql_request.offset(self.page_size)

        # sql_request.request = 'SELECT id,username,rating  FROM core_user  ORDER BY username  LIMIT 10 ;'
        # sql_request.params = []
        sql_request.request = sql_request.request + ';'

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('request: "{}"'.format(sql_request.request))
        print('params: "{}"'.format(sql_request.params))
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        async with self.pool.acquire() as connection:
            items = await connection.fetch(sql_request.request, *sql_request.params)

            return [self.serializer.serialize(item) for item in items]

    async def get(self, item_id) -> object:
        await self.init_pool()

        return {
            'postgresql': 'get',
            'id': item_id
        }

    async def replace_all(self, items: list):
        raise MethodIsNotAllowedException()

    async def create(self, item) -> object:
        raise MethodIsNotAllowedException()

    async def delete_all(self):
        raise MethodIsNotAllowedException()

    async def create_or_replace(self, item_id, item: dict) -> object:
        raise MethodIsNotAllowedException()

    async def update(self, item_id, item: dict) -> object:
        raise MethodIsNotAllowedException()

    async def delete(self, item_id):
        raise MethodIsNotAllowedException()
