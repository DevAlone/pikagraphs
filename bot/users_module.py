from bot.module import Module
from core.models import User, UserRatingEntry, UserCommentsCountEntry, \
                        UserPostsCountEntry, UserHotPostsCountEntry, \
                        UserPlusesCountEntry, UserMinusesCountEntry, \
                        UserSubscribersCountEntry
from pikabot_graphs import settings
from bot.api.client import Client, PikabuError
from django.db.models import F


import asyncio
import time


class UsersModule(Module):
    def __init__(self):
        super(UsersModule, self).__init__('users_module')

    async def _process(self):
        with Client() as client:
            tasks = []

            for user in User.objects.filter(is_updated=True)\
                    .filter(last_update_timestamp__lte=int(time.time()) - F('updating_period')):
                tasks.append(self._call_coroutine_with_logging_exception(self._process_user(user, client)))
                if len(tasks) > 10:
                    await asyncio.wait(tasks)
                    tasks.clear()

            if len(tasks) > 0:
                await asyncio.wait(tasks)

    async def _process_user(self, user, client):
        self._logger.debug('start processing user {}'.format(user.username))

        user.last_update_timestamp = int(time.time())
        user.save()

        try:
            user_data = await client.get_user_profile(user.username)
            user_data = user_data['user']
            user_data['rating'] = int(float(user_data['rating']))
        except PikabuError as ex:
            self._calculate_user_updating_period(user, False)
            user.save()
            raise ex

        was_data_changed = False
        if user.rating != user_data['rating'] or \
                user.comments_count != user_data['comments_count'] or \
                user.posts_count != user_data['stories_count'] or \
                user.hot_posts_count != user_data['stories_hot_count'] or \
                user.pluses_count != user_data['pluses_count'] or \
                user.minuses_count != user_data['minuses_count']:
            was_data_changed = True

        if 'subscribers_count' in user_data:
            if user.subscribers_count != user_data['subscribers_count']:
                was_data_changed = True
        else:
            self._logger.info("subscribers_count disappeared")

        if 'is_rating_ban' in user_data:
            if user.is_rating_ban != user_data['is_rating_ban']:
                was_data_changed = True
        else:
            self._logger.info("is_rating_ban disappeared")

        self._calculate_user_updating_period(user, was_data_changed)

        user.rating = user_data['rating']
        if user_data['avatar']:
            user.avatar_url = user_data['avatar']
        else:
            user.avatar_url = "https://cs.pikabu.ru/images/def_avatar/def_avatar_96.png"
        user.comments_count = user_data['comments_count']
        user.posts_count = user_data['stories_count']
        user.hot_posts_count = user_data['stories_hot_count']
        user.pluses_count = user_data['pluses_count']
        user.minuses_count = user_data['minuses_count']
        user.last_update_timestamp = int(time.time())

        try:
            user.subscribers_count = user_data['subscribers_count']
        except KeyError:
            pass
        try:
            user.is_rating_ban = user_data['is_rating_ban']
        except KeyError:
            pass

        user.save()

        self._save_model_if_last_is_not_the_same(UserRatingEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.rating))

        self._save_model_if_last_is_not_the_same(UserCommentsCountEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.comments_count))

        self._save_model_if_last_is_not_the_same(UserPostsCountEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.posts_count))

        self._save_model_if_last_is_not_the_same(UserHotPostsCountEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.hot_posts_count))

        self._save_model_if_last_is_not_the_same(UserPlusesCountEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.pluses_count))

        self._save_model_if_last_is_not_the_same(UserMinusesCountEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.minuses_count))

        self._save_model_if_last_is_not_the_same(UserSubscribersCountEntry(
            timestamp=user.last_update_timestamp,
            user=user,
            value=user.subscribers_count))

        self._logger.debug('end processing user {}'.format(user.username))

    def _calculate_user_updating_period(self, user, was_data_changed):
        if user.username == 'apres':
            print('was_data_changed: {}'.format(was_data_changed))

        delta = abs((int(time.time()) - user.last_update_timestamp) / 4)
        if delta > settings.USERS_MODULE['MAX_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MAX_UPDATING_DELTA']
        elif delta < settings.USERS_MODULE['MIN_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MIN_UPDATING_DELTA']

        if user.username == 'apres':
            print('delta: {}'.format(delta))

        if was_data_changed:
            user.updating_period -= delta
        else:
            user.updating_period += delta

        if user.username == 'apres':
            self._logger.error('before: {}'.format(user.updating_period))

        if user.updating_period < settings.USERS_MODULE['MIN_UPDATING_PERIOD']:
            user.updating_period = settings.USERS_MODULE['MIN_UPDATING_PERIOD']
        elif user.updating_period > settings.USERS_MODULE['MAX_UPDATING_PERIOD']:
            user.updating_period = settings.USERS_MODULE['MAX_UPDATING_PERIOD']

        if user.username == 'apres':
            self._logger.error('after: {}'.format(user.updating_period))

            self._logger.error("config: {}".format(settings.USERS_MODULE))
            self._logger.error("config max: {}".format(settings.USERS_MODULE['MAX_UPDATING_PERIOD']))

    def _save_model_if_last_is_not_the_same(self, model):
        last_entry = type(model).objects.filter(user=model.user).last()

        if last_entry is None or int(last_entry.value) != int(model.value):
            model.save()
