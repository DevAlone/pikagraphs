import asyncpg
import re

from .exceptions import SQLRequestConstructorException


class _PostgreSQL:
    def __init__(self, user: str, password: str, database: str, max_pool_size: int=10):
        self.user = user
        self.password = password
        self.database = database
        self.max_pool_size = max_pool_size

        self._pool = None

    async def get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=self.user,
                password=self.password,
                database=self.database,
                max_size=self.max_pool_size,
            )

        return self._pool


_postgresql = None


def get_instance(*args, **kwargs):
    global _postgresql
    if _postgresql is None:
        _postgresql = _PostgreSQL(*args, **kwargs)

    return _postgresql


class SQLRequestConstructor:
    def __init__(self):
        self.request = ""
        self.params = []
        self.last_param_number = 0

    def select(self, fields: list):
        self.validate_fields(fields, r'^[0-9a-zA-Z_]+$')
        self._add_sql(' SELECT {} '.format(','.join(fields)), [])
        return self

    def from_table(self, table_name: str):
        self.validate_fields([table_name], r'^[0-9a-zA-Z_]+$')
        self._add_sql(' FROM {} '.format(table_name), [])
        return self

    def order_by(self, fields: list):
        if type(fields) is not list:
            fields = [fields]

        self.validate_fields(fields, r'^-?[0-9a-zA-Z_]+$')
        fields = [(field[1:] + ' DESC' if field.startswith('-') else field) for field in fields]
        self._add_sql(''' ORDER BY {} '''.format(','.join(fields)), [])
        return self

    def limit(self, limiter: int):
        if type(limiter) is not int or limiter < 0:
            raise SQLRequestConstructorException('limiter should be positive integer')
        self._add_sql(' LIMIT $ ', [limiter])
        return self

    def offset(self, value: int):
        if type(value) is not int or value < 0:
            raise SQLRequestConstructorException('offset should be positive integer')
        self._add_sql(' OFFSET $ ', [value])
        return self

    def where(self):
        self._add_sql(' WHERE ', [])
        return self

    def search_by(self, fields, text):
        self.validate_fields(fields, r'^[0-9a-zA-Z_]+$')

        text = text.replace('!', '!!').replace("%", "!%").replace("_", "!_").replace("[", "![")
        text = '%' + text + '%'

        for i, field in enumerate(fields):
            if i != 0:
                self._add_sql(' OR ', [])

            self._add_sql(''' {} ILIKE $ '''.format(field), [text])

        return self

    def _add_sql(self, sql, params: list):
        params.reverse()
        new_sql = ""
        new_params = []

        for ch in sql:
            if ch == '$':
                self.last_param_number += 1
                new_sql += '$' + str(self.last_param_number)
                new_params.append(params.pop())
            else:
                new_sql += ch

        self.request += new_sql
        self.params.extend(new_params)

    def validate_fields(self, fields: list, pattern):
        for field in fields:
            if type(field) is not str or not re.match(pattern, field):
                raise SQLRequestConstructorException('Field "{}" doesn\'t match to pattern "{}"'.format(field, pattern))
