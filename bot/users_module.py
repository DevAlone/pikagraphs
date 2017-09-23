from bot.module import Module
from core.models import User

from core.models import User, UserRatingEntry, UserCommentsCountEntry, \
                        UserPostsCountEntry, UserHotPostsCountEntry, \
                        UserPlusesCountEntry, UserMinusesCountEntry, \
                        UserSubscribersCountEntry

from django.conf import settings

from bot import precise_time
import bot.user

import time
from queue import Queue
import threading
import os
import sys
import traceback


class UsersModule(Module):
    def __init__(self):
        for i in range(settings.USERS_MODULE['NUMBER_OF_WORKERS']):
            threading.Thread(target=self.worker).start()

    def process(self):
        print('processing users file...')
        if not self.usernamesQueue.empty():
            print('users queue is not empty')
            time.sleep(1)
            return

        try:
            with open('usernames') as f:
                for line in f:
                    if (len(line.strip()) > 0):
                        username = line.strip().lower()

                        try:
                            user = User.objects.get(name=username)
                        except User.DoesNotExist:
                            user = User()
                            user.name = username
                            user.save()

                        # if it's time to update, put user in queue
                        if user.lastUpdateTimestamp + \
                                user.updatingPeriod < precise_time.getTimestamp():
                            self.usernamesQueue.put(username)
        except:
            print('file "usernames" not found')

    def saveModelIfLastIsNotTheSame(self, model):
        lastEntry = type(model).objects.filter(user=model.user).last()

        if lastEntry is None or int(lastEntry.value) != int(model.value):
            print('saving...', end='')
            model.save()
        else:
            print('not saving', end='')

        print(' type ' + str(type(model)))

    def processUser(self, username):
        try:
            try:
                user = User.objects.get(name=username)
            except User.DoesNotExist:
                user = User()
                user.name = username
                user.save()

            # sent = False
            # while not sent:
            #     try:
            #         proxies = proxy_utils.getProxyDict(
            #             proxy_receiver_client.getNextProxy(True))
            #         userData = bot.user.getUserProfileData(username, fast=True,
            #                                                proxies=proxies)
            #         sent = True
            #     except Exception as ex:
            #         print('error during get profile: ' + repr(ex))
            #         time.sleep(0.1)

            userData = bot.user.getUserProfileData(username, fast=True)

            wasUserDataChanged = False
            if user.rating != userData['rating'] or \
                            user.commentsCount != userData['commentsCount'] or \
                            user.postsCount != userData['postsCount'] or \
                            user.hotPostsCount != userData['hotPostsCount'] or \
                            user.plusesCount != userData['plusesCount'] or \
                            user.minusesCount != userData['minusesCount']:
                wasUserDataChanged = True
            try:
                if user.subscribersCount != userData['subscribersCount']:
                    wasUserDataChanged = True
            except KeyError:
                pass
            try:
                if user.isRatingBan != userData['isRatingBan']:
                    wasUserDataChanged = True
            except KeyError:
                pass

            delta = abs((precise_time.getTimestamp() - user.lastUpdateTimestamp) / 4)
            if delta > settings.USERS_MODULE['MAX_UPDATING_DELTA']:
                delta = settings.USERS_MODULE['MAX_UPDATING_DELTA']
            if wasUserDataChanged:
                user.updatingPeriod -= settings.USERS_MODULE['MIN_UPDATING_DELTA']  # * 1.5
                user.updatingPeriod -= delta  * 1.5
            else:
                user.updatingPeriod += settings.USERS_MODULE['MIN_UPDATING_DELTA']
                user.updatingPeriod += delta

            if user.updatingPeriod < settings.USERS_MODULE['MIN_UPDATING_PERIOD']:
                user.updatingPeriod = settings.USERS_MODULE['MIN_UPDATING_PERIOD']
            elif user.updatingPeriod > settings.USERS_MODULE['MAX_UPDATING_PERIOD']:
                user.updatingPeriod = settings.USERS_MODULE['MAX_UPDATING_PERIOD']

            user.rating = userData['rating']
            user.commentsCount = userData['commentsCount']
            user.postsCount = userData['postsCount']
            user.hotPostsCount = userData['hotPostsCount']
            user.plusesCount = userData['plusesCount']
            user.minusesCount = userData['minusesCount']
            user.lastUpdateTimestamp = precise_time.getTimestamp()
            try:
                user.subscribersCount = userData['subscribersCount']
            except KeyError:
                pass
            try:
                user.isRatingBan = userData['isRatingBan']
            except KeyError:
                pass

            user.save()

            self.saveModelIfLastIsNotTheSame(UserRatingEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.rating))

            self.saveModelIfLastIsNotTheSame(UserCommentsCountEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.commentsCount))

            self.saveModelIfLastIsNotTheSame(UserPostsCountEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.postsCount))

            self.saveModelIfLastIsNotTheSame(UserHotPostsCountEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.hotPostsCount))

            self.saveModelIfLastIsNotTheSame(UserPlusesCountEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.plusesCount))

            self.saveModelIfLastIsNotTheSame(UserMinusesCountEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.minusesCount))

            self.saveModelIfLastIsNotTheSame(UserSubscribersCountEntry(
                timestamp=user.lastUpdateTimestamp,
                user=user,
                value=user.subscribersCount))

            print(username + ':' + str(userData))
        except Exception as ex:
            # TODO: find where is list index out of range
            # It would be great to add logging of this shit here

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Exception:', exc_type, fname, exc_tb.tb_lineno)

            print('Traceback: ', traceback.format_exc())

            print(ex.__repr__())
            print('\t{0}'.format(ex.args))
        except:
            print('error durint processing user ' + username)

    def worker(self):
        while True:
            time.sleep(0.5)

            item = None
            item = self.usernamesQueue.get()

            if item is not None:
                print('start processing user ' + item)
                self.processUser(item)
                print('end processing user ' + item)

                self.usernamesQueue.task_done()

    usernamesQueue = Queue()
