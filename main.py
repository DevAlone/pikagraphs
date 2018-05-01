#!/usr/bin/env python3

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
            CommunitiesModule(),
            ParseAllUsersModule(),
        ]

    tasks = [module.process() for module in modules]

    loop.run_until_complete(asyncio.gather(*tasks))
