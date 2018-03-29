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
                self.authorize_client(client)

            try:
                for _ in range(self.processing_cycles):
                    await self._call_coroutine_with_logging_exception(
                        self._process_as_user(client))
            except BaseException as ex:
                self._logger.exception(ex)
                await asyncio.sleep(10)

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
        last_id = self.get_last_id() + 1

        tasks = []

        for i in range(last_id, last_id + self.parsing_gap_size):
            tasks.append(self.add_note(i, client))

        await asyncio.gather(*tasks)
        tasks.clear()

        notes = await self.get_notes(client)

        max_user_id = 0

        for note in notes:
            max_user_id = max(max_user_id, note['user_id'])

            tasks.append(self.process_note(note))

        await asyncio.gather(*tasks)
        tasks.clear()

        # if max_user_id == 0:
        #     self._logger.error("max_user_id == 0")
        #     max_user_id = last_id + self.parsing_gap_size

        if max_user_id != 0:
            self.set_last_id(max_user_id)

    def get_last_id(self):
        try:
            with open('.parse_all_users_module_last_id') as file:
                return int(file.readline().strip())
        except FileNotFoundError:
            self.set_last_id(1)
            return self.get_last_id()

    @staticmethod
    def set_last_id(last_id: int):
        with open('.parse_all_users_module_last_id', 'w') as file:
            file.write(str(last_id))

    async def add_note(self, user_id: int, client):
        note_text = str(random.randint(1, 999999))
        self._logger.debug('adding note "{}" for user with id "{}"'.format(
            note_text, user_id))

        try:
            await client.user_note_set(note_text, user_id)
        except PikabuException as ex:
            message = str(ex).strip()
            if message == 'Добавлять заметку самому себе деструктивно и неразумно' \
                    or message == 'Указанный пользователь не найден':
                self._logger.warning(
                    'Пользователь с id "{}" не найден'.format(user_id))
            else:
                raise ex

    async def get_notes(self, client):
        self._logger.debug('getting notes...')
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
        self._logger.debug('processing note...')

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
