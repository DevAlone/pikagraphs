#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client
from lxml import html
import re
import threading
from queue import Queue
import time
import random
import ntplib

import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pikabot_graphs.settings")
django.setup()

from core.models import User, UserRatingEntry, UserCommentsCountEntry, \
                        UserPostsCountEntry, UserHotPostsCountEntry, \
                        UserPlusesCountEntry, UserMinusesCountEntry

# constants
NUMBER_OF_WORKERS = 5
# /constants

# globals
timeDelta = None
usernamesQueue = Queue()
# /globals


class UserProfileData:
    rating = 0
    commentsCount = 0
    postsCount = 0
    hotPostsCount = 0
    plusesCount = 0
    minusesCount = 0

    def __str__(self):
        return "{ 'rating': " + str(self.rating) \
            + ", 'commentsCount': " + str(self.commentsCount) \
            + ", 'postsCount': " + str(self.postsCount) \
            + ", 'hotPostsCount': " + str(self.hotPostsCount) \
            + ", 'plusesCount': " + str(self.plusesCount) \
            + ", 'minusesCount': " + str(self.minusesCount) + " }"

    def __repr__(self):
        return self.__str__()


def getUserProfileData(username):
    userData = UserProfileData()

    connection = http.client.HTTPSConnection("pikabu.ru", timeout=15)
    connection.request("GET", "/profile/" + username)
    response = connection.getresponse()

    data = response.read()

    tree = html.fromstring(data)

    try:
        userData.rating = int(tree.xpath("\
        .//span[@class='b-user-profile__label' and text()=\"рейтинг\"]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    except:
        userData.rating = None

    userData.commentsCount = int(tree.xpath("\
        .//span[@class='b-user-profile__label' and text()=\"комментариев\"]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    userData.postsCount = int(tree.xpath("\
        .//span[@class='b-user-profile__label' and text()=\"добавил постов\"]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    userData.hotPostsCount = int(tree.xpath("\
        .//span[@class='b-user-profile__label' \
        and starts-with(text(), \", из них в \")]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    userPlusesMinusesCount = tree.xpath("\
        .//span[@class='b-user-profile__label' and text()=\"поставил\"]\
        /following-sibling::span[@class='b-user-profile__value']")[0]\
        .text_content()

    matches = re.search(r'^.*?([0-9]+).*плюс.*?([0-9]+).*$',
                        userPlusesMinusesCount, re.DOTALL)

    userData.plusesCount = int(matches.group(1))
    userData.minusesCount = int(matches.group(2))

    return userData


def saveModelIfLastIsNotTheSame(model):
    lastEntry = type(model).objects.filter(user=model.user).last()
    # print('save: ')
    # print('last value: ' + str(lastEntry.value))
    # print('value: ' + str(model.value))
    # print('lastEntry is none: ' + str(lastEntry is None))
    # print('type of last entry value' + str(type(lastEntry.value)))
    # print('type of model value: ' + str(type(model.value)))

    if lastEntry is None or int(lastEntry.value) != int(model.value):
        print('saving...', end='')
        model.save()
    else:
        print('not saving', end='')

    print(' type ' + str(type(model)))


def processUser(username):
    try:
        userData = getUserProfileData(username)

        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            user = User()
            user.name = username
            user.rating = 0

        if userData.rating is not None:
            user.rating = userData.rating
        user.commentsCount = userData.commentsCount
        user.postsCount = userData.postsCount
        user.hotPostsCount = userData.hotPostsCount
        user.plusesCount = userData.plusesCount
        user.minusesCount = userData.minusesCount
        user.lastUpdateTimestamp = int(os.times().elapsed + timeDelta)

        user.save()

        if userData.rating is not None:
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

        print(username + ':' + str(userData))
    except IndexError as ex:
        print('Exception(probably parsing error): ' + str(ex))
    except Exception as ex:
        # TODO: find where is list index out of range
        # It would be great to add logging of this shit here
        print('Exception: ' + str(ex))
    except:
        print('error durint processing user ' + username)


def worker():
    while True:
        time.sleep(1)

        item = None

        item = usernamesQueue.get()

        if item is not None:
            print('start processing user ' + item)
            processUser(item)
            print('end processing user ' + item)

            usernamesQueue.task_done()
            time.sleep(random.randint(1, 5))
        # else:
        #     print('waiting for user...')


if __name__ == "__main__":
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

    for i in range(NUMBER_OF_WORKERS):
        threading.Thread(target=worker).start()

    while(True):
        print('processing file...')

        try:
            with open('usernames') as f:
                for line in f:
                    if(len(line.strip()) > 0):
                        usernamesQueue.put(line.strip().lower())
        except:
            print('file "usernames" not found')

        if usernamesQueue.empty():
            print('queue is empty')
            time.sleep(1)
        else:
            usernamesQueue.join()
