import json

from bot.module import Module
from core.models import User
from pikabot_graphs import settings
from bot.api.pikabu_api.mobile import MobilePikabu as Client, PikabuException as PikabuError
from .db import DB

import copy
import asyncio
import time


class UsersModule(Module):
    processing_period = 10
    # processing_period = 1

    def __init__(self):
        super(UsersModule, self).__init__('users_module')
        self.db = DB.get_instance()
        self.pool = None

    async def _process(self):
        if self.pool is None:
            self.pool = await self.db.get_pool()

        with Client(requests_only_over_proxy=False) as client:
            tasks = []

            async with self.pool.acquire() as connection:
                # TODO: consider using cursor
                users = await connection.fetch('''
                    SELECT * FROM core_user 
                    WHERE is_updated = true and last_update_timestamp <= $1 - updating_period LIMIT $2''',
                    int(time.time()), settings.BOT_CONCURRENT_TASKS)

                for user in users:
                    tasks.append(self._call_coroutine_with_logging_exception(self.process_user(user, client)))

            if tasks:
                await asyncio.wait(tasks)

    async def process_user(self, user: dict, client):
        self._logger.debug('start processing user {}'.format(user['username']))

        try:
            return await self._process_user(user, client)
        except PikabuError as ex:
            updating_period = self._calculate_user_updating_period(user, False)
            async with self.pool.acquire() as connection:
                await connection.execute('''UPDATE core_user SET updating_period = $1, last_update_timestamp = $2
                                WHERE id = $3''', updating_period, int(time.time()), user['id'])
            raise ex
        except BaseException as ex:
            async with self.pool.acquire() as connection:
                await connection.execute('''UPDATE core_user SET last_update_timestamp = $1 WHERE id = $2''',
                                         int(time.time()), user['id'])
            raise ex

    async def _process_user(self, sql_user: dict, client):
        user_data = await client.user_profile_get(sql_user['username'])
        await self._update_user(sql_user, user_data['user'], self._logger)

    @staticmethod
    def record_to_user(sql_user: dict) -> User:
        user = User()

        user.pk = sql_user['id']
        user.pikabu_id = sql_user['pikabu_id']
        user.username = sql_user['username']
        user.avatar_url = sql_user['avatar_url']
        user.rating = sql_user['rating']
        user.comments_count = sql_user['comments_count']
        user.posts_count = sql_user['posts_count']
        user.hot_posts_count = sql_user['hot_posts_count']
        user.pluses_count = sql_user['pluses_count']
        user.minuses_count = sql_user['minuses_count']
        user.subscribers_count = sql_user['subscribers_count']
        user.is_rating_ban = sql_user['is_rating_ban']
        user.gender = sql_user['gender']
        user.approved = sql_user['approved']
        user.awards = sql_user['awards']
        user.signup_timestamp = sql_user['signup_timestamp']
        user.info = sql_user['info']
        user.updating_period = sql_user['updating_period']
        user.is_updated = sql_user['is_updated']
        user.last_update_timestamp = sql_user['last_update_timestamp']

        return user

    async def _update_user(self, sql_user: dict, user_data: dict, logger):
        current_timestamp = int(time.time())
        logger.debug('start processing user {}'.format(sql_user['username']))

        user = self.record_to_user(sql_user)

        previous_user_state = copy.copy(user)

        user.rating = int(float(user_data['rating']))

        if user_data['avatar']:
            user.avatar_url = str(user_data['avatar'])
        else:
            user.avatar_url = ""

        user.comments_count = int(user_data['comments_count'])
        user.posts_count = int(user_data['stories_count'])
        user.hot_posts_count = int(user_data['stories_hot_count'])
        user.pluses_count = int(user_data['pluses_count'])
        user.minuses_count = int(user_data['minuses_count'])

        user.gender = str(user_data['gender'])
        user.approved = str(user_data['approved'])
        user.awards = json.dumps(user_data['awards'])
        user.signup_timestamp = int(user_data['signup_date'])
        user.pikabu_id = int(user_data['user_id'])

        try:
            user.subscribers_count = int(user_data['subscribers_count'])
        except KeyError:
            logger.warning("subscribers_count disappeared")
        try:
            if type(user_data['is_rating_ban']) is bool:
                user.is_rating_ban = user_data['is_rating_ban']
            else:
                user.is_rating_ban = user_data['is_rating_ban'].lower().strip() == 'true'
        except KeyError:
            logger.warning("is_rating_ban disappeared")

        was_data_changed = False

        if user.rating != previous_user_state.rating or \
                user.comments_count != previous_user_state.comments_count or \
                user.posts_count != previous_user_state.posts_count or \
                user.hot_posts_count != previous_user_state.hot_posts_count or \
                user.pluses_count != previous_user_state.pluses_count or \
                user.minuses_count != previous_user_state.minuses_count:
            was_data_changed = True

        if 'subscribers_count' in user_data:
            if user.subscribers_count != previous_user_state.subscribers_count:
                was_data_changed = True

        if 'is_rating_ban' in user_data:
            if user.is_rating_ban != previous_user_state.is_rating_ban:
                was_data_changed = True

        user.updating_period = self._calculate_user_updating_period(sql_user, was_data_changed)

        user.last_update_timestamp = current_timestamp

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(self.insert_user_sql,
                                         user.username, user.rating, user.comments_count,
                                         user.posts_count, user.hot_posts_count, user.pluses_count,
                                         user.minuses_count, user.subscribers_count, user.is_rating_ban,
                                         user.updating_period, user.avatar_url, user.info,
                                         user.is_updated, user.last_update_timestamp, user.approved,
                                         user.awards, user.gender, user.pikabu_id,
                                         user.signup_timestamp
                                         )

                # await connection.executemany("""
                #     INSERT INTO $1 (timestamp, value, user_id)
                #     SELECT $1, $2, $3
                #     WHERE NOT EXISTS (
                #         SELECT * FROM $1 WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                #     );
                #     """, [
                #     ('core_userratingentry', current_timestamp, user.rating, sql_user['id']),
                #     ('core_usercommentscountentry', current_timestamp, user.comments_count, sql_user['id']),
                #     ('core_userpostscountentry', current_timestamp, user.posts_count, sql_user['id']),
                #     ('core_userhotpostscountentry', current_timestamp, user.hot_posts_count, sql_user['id']),
                #     ('core_userplusescountentry', current_timestamp, user.pluses_count, sql_user['id']),
                #     ('core_userminusescountentry', current_timestamp, user.minuses_count, sql_user['id']),
                #     ('core_usersubscriberscountentry', current_timestamp, user.subscribers_count, sql_user['id'])]
                # )
                await connection.execute(
                    """
                    INSERT INTO core_userratingentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_userratingentry WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                    );""", current_timestamp, user.rating, sql_user['id'])
                await connection.execute(
                    """
                    INSERT INTO core_usercommentscountentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_usercommentscountentry WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                    );""", current_timestamp, user.comments_count, sql_user['id'])
                await connection.execute(
                    """
                    INSERT INTO core_userpostscountentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_userpostscountentry WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                    );""", current_timestamp, user.posts_count, sql_user['id'])
                await connection.execute(
                    """
                    INSERT INTO core_userhotpostscountentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_userhotpostscountentry WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                    );""", current_timestamp, user.hot_posts_count, sql_user['id'])
                await connection.execute(
                    """
                    INSERT INTO core_userplusescountentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_userplusescountentry WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                    );""", current_timestamp, user.pluses_count, sql_user['id'])
                await connection.execute(
                    """
                    INSERT INTO core_userminusescountentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_userminusescountentry WHERE value = $2 and user_id = $3 ORDER BY -id LIMIT 1
                    );""", current_timestamp, user.minuses_count, sql_user['id'])
                await connection.execute(
                    """
                    INSERT INTO core_usersubscriberscountentry (timestamp, value, user_id) 
                    SELECT $1, $2, $3
                    WHERE NOT EXISTS (
                        SELECT * FROM core_usersubscriberscountentry 
                        WHERE value = $2 and user_id = $3 
                        ORDER BY -id 
                        LIMIT 1
                    );""", current_timestamp, user.subscribers_count, sql_user['id'])

        logger.debug('end processing user {}'.format(user.username))

    @staticmethod
    def _calculate_user_updating_period(user: dict, was_data_changed: bool) -> int:
        updating_period = user['updating_period']

        delta = abs((int(time.time()) - user['last_update_timestamp']) / 4)
        if delta > settings.USERS_MODULE['MAX_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MAX_UPDATING_DELTA']
        elif delta < settings.USERS_MODULE['MIN_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MIN_UPDATING_DELTA']

        if was_data_changed:
            updating_period -= settings.USERS_MODULE['RESTORE_UPDATING_PERIOD_COEFFICIENT'] * delta
        else:
            updating_period += delta

        if updating_period < settings.USERS_MODULE['MIN_UPDATING_PERIOD']:
            updating_period = settings.USERS_MODULE['MIN_UPDATING_PERIOD']
        elif updating_period > settings.USERS_MODULE['MAX_UPDATING_PERIOD']:
            updating_period = settings.USERS_MODULE['MAX_UPDATING_PERIOD']

        return updating_period

    insert_user_sql = """
INSERT INTO core_user 
    (username, rating, comments_count, posts_count, hot_posts_count, pluses_count, minuses_count, subscribers_count, 
     is_rating_ban, updating_period, avatar_url, info, is_updated, last_update_timestamp, approved, awards, gender, 
     pikabu_id, signup_timestamp) 
    
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)

ON CONFLICT (username) DO UPDATE 
SET rating = excluded.rating, 
    comments_count = excluded.comments_count, 
    posts_count = excluded.posts_count, 
    hot_posts_count = excluded.hot_posts_count, 
    pluses_count = excluded.pluses_count,
    minuses_count = excluded.minuses_count, 
    subscribers_count = excluded.subscribers_count, 
    is_rating_ban = excluded.is_rating_ban, 
    updating_period = excluded.updating_period, 
    avatar_url = excluded.avatar_url, 
    info = excluded.info, 
    is_updated = excluded.is_updated,
    last_update_timestamp = excluded.last_update_timestamp, 
    approved = excluded.approved, 
    awards = excluded.awards, 
    gender = excluded.gender, 
    pikabu_id = excluded.pikabu_id, 
    signup_timestamp = excluded.signup_timestamp;"""
