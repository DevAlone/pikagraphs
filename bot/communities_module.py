from bot.db import DB
from bot.module import Module
from bot.api.client import Client
from pikabot_graphs import settings

import asyncio
import time


class CommunitiesModule(Module):
    processing_period = settings.COMMUNITIES_MODULE['UPDATING_PERIOD']

    def __init__(self):
        super(CommunitiesModule, self).__init__('communities_module')
        self.db = DB.get_instance()
        self.pool = None

    async def _process(self):
        self.logger.debug('start processing communities')

        if self.pool is None:
            self.pool = await self.db.get_pool()

        with Client() as client:
            tasks = []

            for i in range(1, 10000):
                self.logger.debug('got communities page {}'.format(i))
                res = await client.communities_get(page=i, sort='act', community_type='all')
                communities = res['list']
                if len(communities) == 0:
                    break

                for community in communities:
                    tasks.append(self._call_coroutine_with_logging_exception(self._process_community(community)))
                    if len(tasks) > settings.BOT_CONCURRENT_TASKS:
                        await asyncio.wait(tasks)
                        tasks.clear()

            if tasks:
                await asyncio.wait(tasks)
                tasks.clear()

    async def _process_community(self, json_data):
        community_url_name = json_data['link_name'].lower()
        current_timestamp = int(time.time())

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    '''
                    INSERT INTO communities_app_community 
                        (url_name, name, avatar_url, background_image_url, 
                         subscribers_count, stories_count, last_update_timestamp)
                    VALUES ($1, '', '', '', 0, 0, 0)
                    ON CONFLICT (url_name) DO NOTHING;
                    ''', community_url_name
                )

                community_sql = await connection.fetchrow(
                    '''
                    SELECT * FROM communities_app_community 
                    WHERE url_name = $1
                    ''', community_url_name)

                if community_sql['last_update_timestamp'] + settings.COMMUNITIES_MODULE['UPDATING_PERIOD'] >= \
                        current_timestamp:
                    return

                self.logger.debug('start processing community {}'.format(community_url_name))

                subscribers_count = json_data['subscribers']
                stories_count = json_data['stories']
                name = json_data['name']

                await connection.execute(
                    '''
                    UPDATE communities_app_community
                    SET 
                        name = $1,
                        subscribers_count = $2, 
                        stories_count = $3,
                        description = $4,
                        avatar_url = $5,
                        background_image_url = $6,
                        last_update_timestamp = $7
                    WHERE id = $8
                    ''', name, subscribers_count, stories_count, json_data['description'], json_data['avatar_url'],
                    json_data['bg_image_url'], current_timestamp, community_sql['id']
                )

                await connection.execute(
                    '''
                    INSERT INTO communities_app_communitycountersentry 
                        (timestamp, subscribers_count, stories_count, community_id) 
                    SELECT $1, $2, $3, $4
                    WHERE NOT EXISTS (
                        SELECT * FROM communities_app_communitycountersentry 
                        WHERE subscribers_count = $2 and stories_count = $3 and community_id = $4 ORDER BY -id LIMIT 1
                    );''', current_timestamp, subscribers_count, stories_count, community_sql['id']
                )

        self.logger.debug('end processing community {}'.format(community_url_name))
#
#     insert_community_sql = """
# INSERT INTO communities_app_community
#     (url_name, name, description, avatar_url, background_image_url,
#      subscribers_count, stories_count, last_update_timestamp)
#
#     VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
#
# ON CONFLICT (url_name) DO UPDATE
# SET name = excluded.name,
#     description = excluded.description,
#     avatar_url = excluded.avatar_url,
#     background_image_url = excluded.background_image_url,
#     subscribers_count = excluded.subscribers_count,
#     stories_count = excluded.stories_count,
#     last_update_timestamp = excluded.last_update_timestamp;"""
