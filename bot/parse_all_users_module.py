import os

from bot.api.pikabu_api.pikabu import PikabuException
from bot.db import DB
from bot.module import Module
from bot.api.client import Client

import json
import asyncio
import random

from pikabot_graphs import settings


class ParseAllUsersModule(Module):
    processing_period = settings.PARSE_ALL_USERS_MODULE['PROCESSING_PERIOD']
    parsing_gap_size = settings.PARSE_ALL_USERS_MODULE['PROCESSING_GAP_SIZE']
    processing_cycles = settings.PARSE_ALL_USERS_MODULE['PROCESSING_CYCLES']

    def __init__(self):
        super(ParseAllUsersModule, self).__init__('parse_all_users_module')
        self.db = DB.get_instance()
        self.pool = None

    async def _process(self):
        try:
            with open('.parse_all_users_module_user_state', 'r') as file:
                state = json.loads(file.readline().strip())
        except FileNotFoundError:
            state = None

        with Client(saved_state=state) as client:
            if state is None:
                await self.authorize_client(client)

            for _ in range(self.processing_cycles):
                await self._process_as_user(client)

    async def authorize_client(self, client):
        if settings.PARSE_ALL_USERS_MODULE['USERNAME'] is None or settings.PARSE_ALL_USERS_MODULE['PASSWORD'] is None:
            raise Exception("Please, add user")

        await client.login(
            settings.PARSE_ALL_USERS_MODULE['USERNAME'],
            settings.PARSE_ALL_USERS_MODULE['PASSWORD'],
        )
        with open('.parse_all_users_module_user_state', 'w') as file:
            file.write(json.dumps(client.get_state()))

    async def _process_as_user(self, client):
        last_id = (await self.get_last_id()) + 1

        tasks = [
            self.add_note(i, client)
            for i in range(last_id, last_id + self.parsing_gap_size)
        ]

        await asyncio.gather(*tasks)
        tasks.clear()

        notes = await self.get_notes(client)

        tasks = [
            self.process_note(note)
            for note in notes
        ]

        await asyncio.gather(*tasks)
        tasks.clear()

    async def get_last_id(self):
        async with (await self.db.get_pool()).acquire() as connection:
            max_id = await connection.fetchval('SELECT MAX(pikabu_id) FROM core_pikabuuser')
            return max_id if max_id is not None else 0

    # @staticmethod
    # def set_last_id(last_id: int):
    #     with open('.parse_all_users_module_last_id', 'w') as file:
    #         file.write(str(last_id))

    async def add_note(self, user_id: int, client):
        note_text = str(random.randint(1, 999999))
        self.logger.debug('adding note "{}" for user with id "{}"'.format(
            note_text, user_id))

        try:
            await client.user_note_set(note_text, user_id)
        except PikabuException as ex:
            message = str(ex).strip()
            if message.lower() == 'добавлять заметку самому себе деструктивно и неразумно' \
                    or message == 'Указанный пользователь не найден':
                self.logger.debug(
                    'Пользователь с id "{}" не найден'.format(user_id))
            else:
                raise ex

    async def get_notes(self, client):
        self.logger.debug('getting notes...')
        result = []

        while True:
            response = await client.user_notes_get()
            notes = response['notes']

            tasks = []

            if not notes:
                break

            for note in notes:
                result.append({
                    'user_name': note['user_name'],
                    'user_id': int(note['user_id'])
                })
                tasks.append(client.user_note_set("", int(note['user_id'])))
                if len(tasks) > 10:
                    await asyncio.gather(*tasks)
                    tasks.clear()

            if tasks:
                await asyncio.gather(*tasks)

        return result

    async def process_note(self, note):
        self.logger.debug('processing note...')

        noted_user_id = note['user_id']
        noted_user_name = note['user_name']

        async with (await self.db.get_pool()).acquire() as connection:
            await connection.execute('''
                INSERT INTO core_pikabuuser
                    (pikabu_id, username, is_processed)
                VALUES ($1, $2, false)

                ON CONFLICT (pikabu_id) DO UPDATE
                SET username = excluded.username;
                ''', noted_user_id, noted_user_name)
