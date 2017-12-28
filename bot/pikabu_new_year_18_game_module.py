from bot.module import Module
from bot import precise_time
from bot.api.client import Client

from pikabu_new_year_18_game_app.models import ScoreBoardEntry, ScoreEntry
from django.conf import settings

import aiohttp
import json
import time


class PikabuNewYear18GameModule(Module):
    processPeriod = 1 * 60

    def __init__(self):
        super(PikabuNewYear18GameModule, self).__init__('pikabu_new_year_18_game_module')

    async def _process(self):
        self._logger.debug("pikabu_new_year_18_game_module is processing...")
        TOP_URL = "https://pikabu.ru/page/newyear2018/api/controller.php?action=get_top"
        async with aiohttp.ClientSession() as session:
            async with session.get("http://d3d.info:55555/get/best/http/proxy/") as resp:
                proxy_url = await resp.text()

            async with session.get(TOP_URL, proxy=proxy_url) as response:
                json_response = json.loads(await response.text())
                data = json_response["data"]
                scoreboard = ScoreBoardEntry(parse_timestamp=int(time.time()))
                scoreboard.save()

                for item in data:
                    score = ScoreEntry()
                    score.username = item["name"]
                    score.avatar_url = item["avatar"]
                    score.score = item["score"]
                    score.date = item["date"]
                    score.scoreboard_entry = scoreboard
                    score.save()