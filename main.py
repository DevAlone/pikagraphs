#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bot.init_django_models
from bot import precise_time

from bot.users_module import UsersModule
from bot.communities_module import CommunitiesModule

if __name__ == "__main__":
    precise_time.init()

    modules = [
        UsersModule(),
        CommunitiesModule()
    ]

    while(True):
        for module in modules:
            if module.lastProcessTimestamp + module.processPeriod \
                < precise_time.getTimestamp():
                module.process()
                module.lastProcessTimestamp = precise_time.getTimestamp()
