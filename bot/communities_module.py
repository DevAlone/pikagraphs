from bot import api
from bot.module import Module
from bot import precise_time

from communities_app.models import Community, CommunityCountersEntry
from django.conf import settings

import time
import threading
import json
from queue import Queue


class CommunitiesModule(Module):
    def __init__(self):
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()

    def process(self):
        if not self.communitiesQueue.empty():
            print('communities queue is not empty')
            return

        print('processing communities file...')

        try:
            with open('communities') as f:
                for line in f:
                    if len(line.strip()) > 0:
                        communityUrlName = line.strip().replace('\n', '').lower()

                        try:
                            community = Community.objects.get(urlName=communityUrlName)
                        except Community.DoesNotExist:
                            community = Community()
                            community.urlName = communityUrlName
                            community.save()

                        # if it's time to update, put community in queue
                        if community.lastUpdateTimestamp + \
                                settings.COMMUNITIES_MODULE['UPDATING_PERIOD'] < precise_time.getTimestamp():
                            self.communitiesQueue.put(communityUrlName)
                            community.lastUpdateTimestamp = precise_time.getTimestamp()
        except:
            print('file "communities" not found')

    def processCommunity(self, communityUrlName):
        try:
            res = api.getCommunity(communityUrlName)
            jsonData = json.loads(res.text)['response']
            name = jsonData['name']
            subscribersCount = jsonData['subscribers']
            storiesCount = jsonData['stories']
            name = jsonData['name']

            try:
                community = Community.objects.get(urlName=communityUrlName)
            except Community.DoesNotExist:
                community = Community()
                community.urlName = communityUrlName
                community.save()

            wasDataChanged = False
            if community.subscribersCount != subscribersCount \
                    or community.storiesCount != storiesCount \
                    or community.name != name:
                wasDataChanged = True

            community.name = name
            community.subscribersCount = subscribersCount
            community.storiesCount = storiesCount
            community.lastUpdateTimestamp = precise_time.getTimestamp()
            community.save()

            self.saveCountersIfLastIsNotTheSame(CommunityCountersEntry(
                timestamp=community.lastUpdateTimestamp,
                community=community,
                subscribersCount=subscribersCount,
                storiesCount=storiesCount
            ))

            print('community {} is processed'.format(communityUrlName))
        except Exception as ex:
            print('error in communities module: ' + repr(ex))
        except:
            print('error in communities module')

    def saveCountersIfLastIsNotTheSame(self, model):
        lastEntry = type(model).objects.filter(community=model.community).last()

        if lastEntry is None \
                or int(lastEntry.subscribersCount) != int(model.subscribersCount) \
                or int(lastEntry.storiesCount) != int(model.storiesCount):
            print('saving...', end='')
            model.save()
        else:
            print('not saving', end='')

        print(' type ' + str(type(model)))

    def worker(self):
        while True:
            time.sleep(0.5)

            item = None
            item = self.communitiesQueue.get()

            if item is not None:
                print('start processing community ' + item)
                self.processCommunity(item)
                print('end processing community ' + item)

                self.communitiesQueue.task_done()

    communitiesQueue = Queue()
    thread = None