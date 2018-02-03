from bot.api.pikabu_api.pikabu import PikabuException
from bot.module import Module
from bot.api.pikabu_api.mobile import MobilePikabu as Client

from core.models import PikabuUser

import json
import asyncio
import random


class ParseAllUsersModule(Module):
    processing_period = 10
    parsing_gap_size = 10
    processing_cycles = 1

    def __init__(self):
        super(ParseAllUsersModule, self).__init__('parse_all_users_module')

    async def _process(self):
        with open('.parse_all_users_module_user_state') as file:
            state = json.loads(file.readline().strip())

        with Client(requests_only_over_proxy=False, saved_state=state) as client:
            try:
                for _ in range(self.processing_cycles):
                    await self._call_coroutine_with_logging_exception(self._process_as_user(client))
            except BaseException as ex:
                self._logger.exception(ex)
                await asyncio.sleep(10)

    async def _process_as_user(self, client):
        last_id = self.get_last_id()

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

        if max_user_id == 0:
            self._logger.error("max_user_id == 0")
            max_user_id = last_id + self.parsing_gap_size

        self.set_last_id(max_user_id + 1)

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
        self._logger.debug('adding note "{}" for user with id "{}"'.format(note_text, user_id))

        try:
            await client.user_note_set(note_text, user_id)
        except PikabuException as ex:
            message = str(ex).strip()
            if message == 'Добавлять заметку самому себе деструктивно и неразумно':
                    # or message == 'Указанный пользователь не найден':
                self._logger.warning('Пользователь с id "{}" не найден'.format(user_id))
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

        try:
            user = PikabuUser.objects.get(pikabu_id=noted_user_id)
        except PikabuUser.DoesNotExist:
            user = PikabuUser(pikabu_id=noted_user_id)

        user.username = noted_user_name
        user.save()
