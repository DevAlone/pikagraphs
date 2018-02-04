import copy
import json

import os

from bot.module import Module
from core.models import User, UserRatingEntry, UserCommentsCountEntry, UserPostsCountEntry, UserHotPostsCountEntry
from core.models import UserPlusesCountEntry, UserMinusesCountEntry, UserSubscribersCountEntry, PikabuUser
from pikabot_graphs import settings
# from bot.api.client import Client, PikabuError
from bot.api.pikabu_api.mobile import MobilePikabu as Client, PikabuException as PikabuError
from bot.api.pikabu_api.proxy_provider import ProxyManager1

from django.db.models import F

import asyncio
import time


class UsersModule(Module):
    processing_period = 10
    # processing_period = 1

    def __init__(self):
        super(UsersModule, self).__init__('users_module')
        self.proxy_provider = ProxyManager1.get_instance()

    async def _process(self):
        with Client(requests_only_over_proxy=False) as client:
            tasks = []

            for user in User.objects.filter(is_updated=True)\
                    .filter(last_update_timestamp__lte=int(time.time()) - F('updating_period')):
                tasks.append(self._call_coroutine_with_logging_exception(self.process_user(user, client)))
                if len(tasks) > 100:
                    await asyncio.wait(tasks)
                    tasks.clear()

            if len(tasks) > 0:
                await asyncio.wait(tasks)

            # await self.process_pikabu_users()

    # async def process_pikabu_users(self):
    #     with open('.push_users_info_db', 'r') as file:
    #         for _ in range(10):
    #             json_data = json.loads(file.readline().strip())
    #             username = json_data['user_name'].strip().lower()
    #
    #             try:
    #                 user = User.objects.get(username=username)
    #             except User.DoesNotExist:
    #                 user = User()
    #                 user.username = username
    #
    #             self._update_user(user, json_data, self._logger)

    async def process_user(self, user, client):
        self._logger.debug('start processing user {}'.format(user.username))

        try:
            return await self._process_user(user, client)
        except PikabuError as ex:
            self._calculate_user_updating_period(user, False)
            user.last_update_timestamp = int(time.time())
            user.save()
            raise ex
        except BaseException as ex:
            user.last_update_timestamp = int(time.time())
            user.save()
            raise ex

    async def _process_user(self, user, client):
        user_data = await client.user_profile_get(user.username)
        self._update_user(user, user_data['user'], self._logger)

    @staticmethod
    def _update_user(user, user_data, logger, save_graphs=True):
        logger.debug('start processing user {}'.format(user.username))

        user_data['rating'] = int(float(user_data['rating']))
        user_data['comments_count'] = int(user_data['comments_count'])
        user_data['stories_count'] = int(user_data['stories_count'])
        user_data['stories_hot_count'] = int(user_data['stories_hot_count'])
        user_data['pluses_count'] = int(user_data['pluses_count'])
        user_data['minuses_count'] = int(user_data['minuses_count'])
        user_data['subscribers_count'] = int(user_data['subscribers_count'])
        user_data['signup_date'] = int(user_data['signup_date'])
        user_data['user_id'] = int(user_data['user_id'])

        if type(user_data['is_rating_ban']) is not bool:
            user_data['is_rating_ban'] = user_data['is_rating_ban'].lower().strip() == 'true'

        previous_user_state = copy.copy(user)

        user.rating = user_data['rating']
        if user_data['avatar']:
            user.avatar_url = user_data['avatar']
        else:
            user.avatar_url = ""

        user.comments_count = user_data['comments_count']
        user.posts_count = user_data['stories_count']
        user.hot_posts_count = user_data['stories_hot_count']
        user.pluses_count = user_data['pluses_count']
        user.minuses_count = user_data['minuses_count']

        user.gender = str(user_data['gender'])
        user.approved = user_data['approved']
        user.awards = user_data['awards']
        user.communities = user_data['communities']
        user.signup_timestamp = user_data['signup_date']
        user.pikabu_id = user_data['user_id']

        try:
            user.subscribers_count = user_data['subscribers_count']
        except KeyError:
            logger.warning("subscribers_count disappeared")
        try:
            user.is_rating_ban = user_data['is_rating_ban']
        except KeyError:
            logger.warning("is_rating_ban disappeared")

        was_data_changed = False

        if user.rating != previous_user_state.rating or user.comments_count != previous_user_state.comments_count or \
                user.posts_count != previous_user_state.posts_count or \
                user.hot_posts_count != previous_user_state.hot_posts_count or \
                user.pluses_count != previous_user_state.pluses_count or \
                user.minuses_count != previous_user_state.minuses_count:
            was_data_changed = True

        if 'subscribers_count' in user_data:
            if user.subscribers_count != previous_user_state.subscribers_count:
                was_data_changed = True

        if 'is_rating_ban' in user_data:
            if user.is_rating_ban != previous_user_state.is_rating_ban:
                was_data_changed = True

        UsersModule._calculate_user_updating_period(user, was_data_changed)

        user.last_update_timestamp = int(time.time())

        logger.debug('start saving user')
        user.save()
        logger.debug('stop saving user')

        if save_graphs:
            logger.debug('start saving graphs')
            UsersModule._save_model_if_last_is_not_the_same(UserRatingEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.rating), logger)

            UsersModule._save_model_if_last_is_not_the_same(UserCommentsCountEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.comments_count), logger)

            UsersModule._save_model_if_last_is_not_the_same(UserPostsCountEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.posts_count), logger)

            UsersModule._save_model_if_last_is_not_the_same(UserHotPostsCountEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.hot_posts_count), logger)

            UsersModule._save_model_if_last_is_not_the_same(UserPlusesCountEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.pluses_count), logger)

            UsersModule._save_model_if_last_is_not_the_same(UserMinusesCountEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.minuses_count), logger)

            UsersModule._save_model_if_last_is_not_the_same(UserSubscribersCountEntry(
                timestamp=user.last_update_timestamp,
                user=user,
                value=user.subscribers_count), logger)
            logger.debug('stop saving graphs')

        logger.debug('end processing user {}'.format(user.username))

    @staticmethod
    def _calculate_user_updating_period(user, was_data_changed):
        delta = abs((int(time.time()) - user.last_update_timestamp) / 4)
        if delta > settings.USERS_MODULE['MAX_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MAX_UPDATING_DELTA']
        elif delta < settings.USERS_MODULE['MIN_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MIN_UPDATING_DELTA']

        if was_data_changed:
            user.updating_period -= delta
        else:
            user.updating_period += delta

        if user.updating_period < settings.USERS_MODULE['MIN_UPDATING_PERIOD']:
            user.updating_period = settings.USERS_MODULE['MIN_UPDATING_PERIOD']
        elif user.updating_period > settings.USERS_MODULE['MAX_UPDATING_PERIOD']:
            user.updating_period = settings.USERS_MODULE['MAX_UPDATING_PERIOD']

    @staticmethod
    def _save_model_if_last_is_not_the_same(model, logger=None):
        if logger is not None:
            logger.debug("start getting last counter...")
        last_entry = type(model).objects.filter(user=model.user).last()
        if logger is not None:
            logger.debug("stop last counter...")

        if last_entry is None or int(last_entry.value) != int(model.value):
            if logger is not None:
                logger.debug("start saving last counter...")
            model.save()
            if logger is not None:
                logger.debug("stop saving last counter...")
