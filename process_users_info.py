import asyncio
import traceback

import os

import bot.init_django_models

from core.models import User, PikabuUser
from bot.users_module import UsersModule
import json
import sys
import logging
from pikabot_graphs import settings
import aiopg


async def process_user(json_data, pool):
    try:
        async with pool.acquire() as connection:
            await UsersModule._update_user_async(json_data, connection)

            async with connection.cursor() as cursor:
                await cursor.execute("""UPDATE core_pikabuuser SET "is_processed" = true WHERE "pikabu_id" = %s""", [
                    json_data['user_id']
                ])
    except BaseException as ex:
        print(type(ex))
        print(ex)
        traceback.print_exc()
        os._exit(1)


async def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(log_handler)

    tasks = []

    pool = await aiopg.create_pool("dbname={} user={} password={} host={}".format(
        settings.DATABASES["default"]["NAME"],
        settings.DATABASES["default"]["USER"],
        settings.DATABASES["default"]["PASSWORD"],
        settings.DATABASES["default"]["HOST"],
    ))

    with open(sys.argv[1], 'r') as file:
        for line in file:
            json_data = json.loads(line.strip())
            json_data = json_data['user']
            logger.info('start processing {}'.format(json_data['user_name']))

            tasks.append(process_user(json_data, pool))

            if len(tasks) > 100:
                await asyncio.wait(tasks)
                tasks.clear()

    if tasks:
        await asyncio.wait(tasks)
        tasks.clear()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""USAGE
        {} DATABASE_FILE
        """.format(sys.argv[0]))
        exit(1)

    asyncio.get_event_loop().run_until_complete(main())
