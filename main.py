#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bot.init_django_models
from bot import precise_time
from bot.users_module import UsersModule
from bot.communities_module import CommunitiesModule

import asyncio

if __name__ == "__main__":
    precise_time.init()
    loop = asyncio.get_event_loop()

    modules = [
        UsersModule(),
        CommunitiesModule()
    ]

    while True:
        tasks = []
        for module in modules:
            if module.lastProcessTimestamp + module.processPeriod < precise_time.getTimestamp():
                tasks.append(asyncio.ensure_future(module.process()))
                module.lastProcessTimestamp = precise_time.getTimestamp()
        if len(tasks) > 0:
            loop.run_until_complete(asyncio.wait(tasks))
        else:
            loop.run_until_complete(asyncio.sleep(1))