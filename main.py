#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bot.init_django_models

from bot.users_module import UsersModule
from bot.communities_module import CommunitiesModule
from bot.pikabu_new_year_18_game_module import PikabuNewYear18GameModule
from bot.parse_all_users_module import ParseAllUsersModule
from pikabot_graphs import settings

import asyncio
import time

# async def pikabu_new_year_18_game_module_executor():
#     # pretty bad solution
#     module = PikabuNewYear18GameModule()
#     while True:
#         await module.process()
#         await asyncio.sleep(module.processPeriod)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    modules = [
        UsersModule(),
        CommunitiesModule(),
        ParseAllUsersModule()
    ]

    # if settings.DEBUG:
    #     modules = [ParseAllUsersModule()]

    # loop.create_task(pikabu_new_year_18_game_module_executor())

    tasks = []

    for module in modules:
        tasks.append(module.process())
        # if module.last_processing_timestamp + module.processing_period < int(time.time()):
        #     tasks.append(module.process())
        #     module.lastProcessTimestamp = int(time.time())

    loop.run_until_complete(asyncio.wait(tasks))

