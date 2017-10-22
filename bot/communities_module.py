from bot.module import Module
from bot import precise_time
from bot.api.client import Client

from communities_app.models import Community, CommunityCountersEntry
from django.conf import settings


class CommunitiesModule(Module):
    processPeriod = 10 * 60

    def __init__(self):
        super(CommunitiesModule, self).__init__('communities_module')

    async def _process(self):
        with Client() as client:
            for i in range(1, 10000):
                res = await client.get_communities(page=i, sort='act', community_type='all')
                communities = res['list']
                if len(communities) == 0:
                    break

                for community in communities:
                    self._processCommunity(community, client)

    def _processCommunity(self, json_data, client):
        community_url_name = json_data['link_name']

        try:
            community = Community.objects.get(urlName=community_url_name)
        except Community.DoesNotExist:
            community = Community()
            community.urlName = community_url_name
            community.save()

        if community.lastUpdateTimestamp + settings.COMMUNITIES_MODULE['UPDATING_PERIOD'] >= precise_time.getTimestamp():
            return

        self._logger.debug('start processing community {}'.format(community_url_name))

        subscribers_count = json_data['subscribers']
        stories_count = json_data['stories']
        name = json_data['name']

        community.name = name
        community.subscribersCount = subscribers_count
        community.storiesCount = stories_count
        community.lastUpdateTimestamp = precise_time.getTimestamp()
        community.save()

        self._saveCountersIfLastIsNotTheSame(CommunityCountersEntry(
            timestamp=community.lastUpdateTimestamp,
            community=community,
            subscribersCount=subscribers_count,
            storiesCount=stories_count
        ))

        self._logger.debug('end processing community {}'.format(community_url_name))

    def _saveCountersIfLastIsNotTheSame(self, model):
        lastEntry = type(model).objects.filter(community=model.community).last()

        if lastEntry is None \
                or int(lastEntry.subscribersCount) != int(model.subscribersCount) \
                or int(lastEntry.storiesCount) != int(model.storiesCount):
            model.save()