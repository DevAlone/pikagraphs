from bot.module import Module
from bot import precise_time
from bot.api.client import Client

from communities_app.models import Community, CommunityCountersEntry
from django.conf import settings


class CommunitiesModule(Module):
    processPeriod = settings.COMMUNITIES_MODULE['UPDATING_PERIOD']

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
                    self._process_community(community)

    def _process_community(self, json_data):
        community_url_name = json_data['link_name'].lower()

        try:
            community = Community.objects.get(url_name=community_url_name)
        except Community.DoesNotExist:
            community = Community()
            community.url_name = community_url_name
            community.save()

        community.last_update_timestamp = 0
        community.save()

        if community.last_update_timestamp + settings.COMMUNITIES_MODULE['UPDATING_PERIOD'] \
                >= precise_time.getTimestamp():
            return

        self._logger.debug('start processing community {}'.format(community_url_name))

        subscribers_count = json_data['subscribers']
        stories_count = json_data['stories']
        name = json_data['name']

        community.name = name
        community.subscribers_count = subscribers_count
        community.stories_count = stories_count
        community.description = json_data['description']
        community.avatar_url = json_data['avatar_url']
        community.background_image_url = json_data['bg_image_url']
        community.last_update_timestamp = precise_time.getTimestamp()
        community.save()
        CommunityCountersEntry(
            timestamp=community.last_update_timestamp,
            community=community,
            subscribers_count=subscribers_count,
            stories_count=stories_count
        )
        self._save_counters_if_last_is_not_the_same(CommunityCountersEntry(
            timestamp=community.last_update_timestamp,
            community=community,
            subscribers_count=subscribers_count,
            stories_count=stories_count
        ))

        self._logger.debug('end processing community {}'.format(community_url_name))

    def _save_counters_if_last_is_not_the_same(self, model):
        last_entry = type(model).objects.filter(community=model.community).last()

        if last_entry is None \
                or int(last_entry.subscribers_count) != int(model.subscribers_count) \
                or int(last_entry.stories_count) != int(model.stories_count):
            model.save()
