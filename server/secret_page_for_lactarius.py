import datetime

import asyncpgsa

from models import communities_app_community, communities_app_communitycountersentry
from restycorn.restycorn.exceptions import MethodIsNotAllowedException
from restycorn.restycorn.postgresql_serializer import PostgreSQLSerializer
from restycorn.restycorn.read_only_resource import ReadOnlyResource


def _get_moscow_timestamp(timestamp):
    return timestamp + 3600 * 3


class SecretPageForLactarius(ReadOnlyResource):
    def get(self, item_id) -> object:
        raise MethodIsNotAllowedException()

    async def list(self) -> list:
        sql_request = communities_app_community.select().where(
            communities_app_community.c.url_name == 'leagueofartists'
        )

        item = await asyncpgsa.pg.fetchrow(sql_request)

        counters_entries = await asyncpgsa.pg.fetch(
            communities_app_communitycountersentry.select().where(
                communities_app_communitycountersentry.c.community_id == item['id']
            ) .order_by(
                communities_app_communitycountersentry.c.timestamp
            )
        )

        counters_entries = [PostgreSQLSerializer([
                'id', 'timestamp', 'community_id', 'subscribers_count', 'stories_count'
        ]).serialize(item) for item in counters_entries]

        result_array = []
        last_day = 0
        for entry in counters_entries:
            days_since_epoch = (datetime.datetime.utcfromtimestamp(
                _get_moscow_timestamp(entry['timestamp'])) -
                                datetime.datetime.utcfromtimestamp(0)
                                ).days

            if days_since_epoch > last_day:
                entry['timestamp'] = _get_moscow_timestamp(entry['timestamp'])
                result_array.append(entry)
                last_day = days_since_epoch

        for entry in result_array:
            dt = datetime.datetime.utcfromtimestamp(entry['timestamp'])
            entry['time'] = dt.strftime('%d.%m.%Y %H:%M')

        return result_array


secret_page_for_lactarius = SecretPageForLactarius()
