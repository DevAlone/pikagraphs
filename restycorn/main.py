import asyncio

import asyncpg

import postgresql
from base_resource import BaseResource
from postgresql_read_only_resource import PostgreSQLReadOnlyResource
from server import Server
from exceptions import ResourceItemDoesNotExistException


class TestResource(BaseResource):
    def __init__(self):
        self.db = {}
        self.last_id = 0

    def list(self) -> list:
        return [value for key, value in self.db.items()]

    def replace_all(self, items: list):
        self.db = {}
        for item in items:
            self.create(item)

    def create(self, item) -> object:
        self.last_id += 1
        self.db[self.last_id] = item

        return self.db[self.last_id]

    def delete_all(self):
        self.db.clear()

    def get(self, item_id) -> object:
        item_id = int(item_id)
        if item_id not in self.db:
            raise ResourceItemDoesNotExistException()

        return self.db[item_id]

    def create_or_replace(self, item_id, item: dict) -> object:
        self.db[item_id] = item
        return self.db[item_id]

    def update(self, item_id, item: dict) -> object:
        for key, val in item:
            setattr(self.db[item_id], key, val)

        return self.db[item_id]

    def delete(self, item_id):
        del self.db[item_id]


def main():
    server = Server()
    server.set_base_address('/api')

    db = postgresql.get_instance(
        user='test',
        password='test',
        database='test',
    )

    server.register_resource('users', PostgreSQLReadOnlyResource(
        db=db,
        fields=('id', 'username', 'rating', ),
        table_name='core_user',
        order_by=('id', 'rating', 'username'),
        search_by=('username', ),
    ))
    server.register_resource('users', TestResource())
    server.run()


if __name__ == '__main__':
    main()
    asyncio.get_event_loop().run_until_complete(main())
