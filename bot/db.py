from pikabot_graphs import settings
import asyncpg


class DB:
    @staticmethod
    def get_instance():
        global _db
        return _db

    def __init__(self):
        self._pool = None
        # self.users = UsersModule(self)

    async def get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=settings.DATABASES["default"]["USER"],
                password=settings.DATABASES["default"]["PASSWORD"],
                database=settings.DATABASES["default"]["NAME"],
                max_size=settings.DATABASES["default"]["CONCURRENT_TASKS_COUNT"],
            )

        return self._pool


# class UsersModule:
#     def __init__(self, db):
#         self.db = db
#
#     # async def save_user(self, user):
#     #     pass


_db = DB()
