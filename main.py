#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bot.init_django_models

from pikabot_graphs import settings
from bot.users_module import UsersModule
from bot.communities_module import CommunitiesModule
from bot.parse_all_users_module import ParseAllUsersModule

import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    modules = [
        UsersModule(),
        CommunitiesModule(),
        ParseAllUsersModule()
    ]

    if settings.DEBUG:
        modules = [
            UsersModule(),
            # ParseAllUsersModule(),
        ]

    tasks = []

    for module in modules:
        tasks.append(module.process())
        # if module.last_processing_timestamp + module.processing_period < int(time.time()):
        #     tasks.append(module.process())
        #     module.lastProcessTimestamp = int(time.time())

    loop.run_until_complete(asyncio.wait(tasks))
