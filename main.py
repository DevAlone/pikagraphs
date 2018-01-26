#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bot.init_django_models
from bot import precise_time
from bot.users_module import UsersModule
from bot.communities_module import CommunitiesModule
from bot.pikabu_new_year_18_game_module import PikabuNewYear18GameModule

import asyncio


# async def pikabu_new_year_18_game_module_executor():
#     # pretty bad solution
#     module = PikabuNewYear18GameModule()
#     while True:
#         await module.process()
#         await asyncio.sleep(module.processPeriod)

if __name__ == "__main__":
    precise_time.init()
    loop = asyncio.get_event_loop()

    modules = [
        UsersModule(),
        CommunitiesModule(),
    ]

    # loop.create_task(pikabu_new_year_18_game_module_executor())

    while True:
        tasks = []
        for module in modules:
            if module.lastProcessTimestamp + module.processPeriod < precise_time.getTimestamp():
                tasks.append(module.process())
                module.lastProcessTimestamp = precise_time.getTimestamp()
        if tasks:
            loop.run_until_complete(asyncio.wait(tasks))
        else:
            loop.run_until_complete(asyncio.sleep(1))
