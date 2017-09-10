#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from queue import Queue
import time
import random
import ntplib

import os
import sys

import traceback

import bot.init_django_models

from core.models import User, UserRatingEntry, UserCommentsCountEntry, \
                        UserPostsCountEntry, UserHotPostsCountEntry, \
                        UserPlusesCountEntry, UserMinusesCountEntry, \
                        UserSubscribersCountEntry
import bot.user

# constants
NUMBER_OF_WORKERS = 1
# START_TOR_PORT = 30000
MIN_UPDATING_PERIOD = 20
MAX_UPDATING_PERIOD = 60 * 15
MIN_UPDATING_DELTA = 1
MAX_UPDATING_DELTA = 60
# /constants

# globals
timeDelta = None
usernamesQueue = Queue()
# /globals

def getTimestamp():
    return int(os.times().elapsed + timeDelta)


def saveModelIfLastIsNotTheSame(model):
    lastEntry = type(model).objects.filter(user=model.user).last()

    if lastEntry is None or int(lastEntry.value) != int(model.value):
        print('saving...', end='')
        model.save()
    else:
        print('not saving', end='')

    print(' type ' + str(type(model)))


def processUser(username):
    try:
        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            user = User()
            user.name = username

        userData = bot.user.getUserProfileData(username, fast=True)

        wasUserDataChanged = False
        if      user.rating != userData['rating'] or \
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

        delta = abs((getTimestamp() - user.lastUpdateTimestamp) / 8)
        if delta > MAX_UPDATING_DELTA:
            delta = MAX_UPDATING_DELTA
        if wasUserDataChanged:
            user.updatingPeriod -= MIN_UPDATING_DELTA * 2
            user.updatingPeriod -= delta * 2
        else:
            user.updatingPeriod += MIN_UPDATING_DELTA
            user.updatingPeriod += delta

        if user.updatingPeriod < MIN_UPDATING_PERIOD:
            user.updatingPeriod = MIN_UPDATING_PERIOD
        elif user.updatingPeriod > MAX_UPDATING_PERIOD:
            user.updatingPeriod = MAX_UPDATING_PERIOD

        user.rating = userData['rating']
        user.commentsCount = userData['commentsCount']
        user.postsCount = userData['postsCount']
        user.hotPostsCount = userData['hotPostsCount']
        user.plusesCount = userData['plusesCount']
        user.minusesCount = userData['minusesCount']
        user.lastUpdateTimestamp = getTimestamp()
        try:
            user.subscribersCount = userData['subscribersCount']
        except KeyError:
            pass
        try:
            user.isRatingBan = userData['isRatingBan']
        except KeyError:
            pass

        user.save()

        saveModelIfLastIsNotTheSame(UserRatingEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.rating))

        saveModelIfLastIsNotTheSame(UserCommentsCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.commentsCount))

        saveModelIfLastIsNotTheSame(UserPostsCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.postsCount))

        saveModelIfLastIsNotTheSame(UserHotPostsCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.hotPostsCount))

        saveModelIfLastIsNotTheSame(UserPlusesCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.plusesCount))

        saveModelIfLastIsNotTheSame(UserMinusesCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.minusesCount))

        saveModelIfLastIsNotTheSame(UserSubscribersCountEntry(
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


def worker():
    while True:
        time.sleep(0.5)

        item = None
        item = usernamesQueue.get()

        if item is not None:
            print('start processing user ' + item)
            processUser(item)
            print('end processing user ' + item)

            usernamesQueue.task_done()


def updateTime():
    global timeDelta
    if os.times().elapsed == 0:
        print("Sorry, your platform isn't supported")
        exit(1)

    # get time from internet
    # maybe it needs to be repeated it in thread
    while timeDelta is None:
        try:
            if not os.path.exists('.last_timestamp'):
                with open('.last_timestamp', 'w') as f:
                    f.write(str(0))

            with open('.last_timestamp') as f:
                lastTimestamp = int(float(f.readline()))

            ntpClient = ntplib.NTPClient()
            ntpResponse = ntpClient.request('europe.pool.ntp.org')
            ntpTimestamp = ntpResponse.tx_time
            timeDelta = int(ntpTimestamp - os.times().elapsed)

            if int(ntpTimestamp) < lastTimestamp:
                print('some shit happened')
                exit(1)

            with open('.last_timestamp', 'w') as f:
                f.write(str(int(ntpTimestamp)))
        except Exception as ex:
            print('Error during getting time from NTP')
            raise ex
            time.sleep(1)

    print('time delta is ' + str(timeDelta))


if __name__ == "__main__":
    updateTime()


    for i in range(NUMBER_OF_WORKERS):
        threading.Thread(target=worker).start()

    while(True):
        print('processing file...')

        try:
            with open('usernames') as f:
                for line in f:
                    if(len(line.strip()) > 0):
                        username = line.strip().lower()

                        try:
                            user = User.objects.get(name=username)
                        except User.DoesNotExist:
                            user = User()
                            user.name = username
                            user.save()

                        # if it's time to update, put user in queue
                        if user.lastUpdateTimestamp + user.updatingPeriod < getTimestamp():
                            usernamesQueue.put(username)
        except:
            print('file "usernames" not found')

        if usernamesQueue.empty():
            print('queue is empty')
            time.sleep(1)
        else:
            usernamesQueue.join()
