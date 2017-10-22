from bot.module import Module
from core.models import User, UserRatingEntry, UserCommentsCountEntry, \
                        UserPostsCountEntry, UserHotPostsCountEntry, \
                        UserPlusesCountEntry, UserMinusesCountEntry, \
                        UserSubscribersCountEntry
from pikabot_graphs import settings
from bot.api.client import Client


import asyncio
from bot import precise_time


class UsersModule(Module):
    def __init__(self):
        super(UsersModule, self).__init__('users_module')

    async def _process(self):
        with Client() as client:
            with open('usernames') as f:
                tasks = []
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
                            tasks.append(self._callCoroutineWithLoggingException(self._processUser(username, client)))
                            if len(tasks) > 10:
                                await asyncio.wait(tasks)
                                tasks.clear()
                            user.lastUpdateTimestamp = precise_time.getTimestamp()

                if len(tasks) > 0:
                    await asyncio.wait(tasks)

    async def _processUser(self, username, client):
        self._logger.debug('start processing user {}'.format(username))

        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            user = User()
            user.name = username
            user.save()

        user_data = await client.get_user_profile(username)
        user_data = user_data['user']
        user_data['rating'] = int(float(user_data['rating']))

        was_data_changed = False
        if user.rating != user_data['rating'] or \
                        user.commentsCount != user_data['comments_count'] or \
                        user.postsCount != user_data['stories_count'] or \
                        user.hotPostsCount != user_data['stories_hot_count'] or \
                        user.plusesCount != user_data['pluses_count'] or \
                        user.minusesCount != user_data['minuses_count']:
            was_data_changed = True

        if 'subscribers_count' in user_data:
            if user.subscribersCount != user_data['subscribers_count']:
                was_data_changed = True
        else:
            self._logger.info("subscribers_count disappeared")

        if 'is_rating_ban' in user_data:
            if user.isRatingBan != user_data['is_rating_ban']:
                was_data_changed = True
        else:
            self._logger.info("is_rating_ban disappeared")

        self._calculate_user_updating_period(user, was_data_changed)

        user.rating = user_data['rating']
        user.commentsCount = user_data['comments_count']
        user.postsCount = user_data['stories_count']
        user.hotPostsCount = user_data['stories_hot_count']
        user.plusesCount = user_data['pluses_count']
        user.minusesCount = user_data['minuses_count']
        user.lastUpdateTimestamp = precise_time.getTimestamp()

        try:
            user.subscribersCount = user_data['subscribers_count']
        except KeyError:
            pass
        try:
            user.isRatingBan = user_data['is_rating_ban']
        except KeyError:
            pass

        user.save()

        self._saveModelIfLastIsNotTheSame(UserRatingEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.rating))

        self._saveModelIfLastIsNotTheSame(UserCommentsCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.commentsCount))

        self._saveModelIfLastIsNotTheSame(UserPostsCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.postsCount))

        self._saveModelIfLastIsNotTheSame(UserHotPostsCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.hotPostsCount))

        self._saveModelIfLastIsNotTheSame(UserPlusesCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.plusesCount))

        self._saveModelIfLastIsNotTheSame(UserMinusesCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.minusesCount))

        self._saveModelIfLastIsNotTheSame(UserSubscribersCountEntry(
            timestamp=user.lastUpdateTimestamp,
            user=user,
            value=user.subscribersCount))

        self._logger.debug('end processing user {}'.format(username))

    def _calculate_user_updating_period(self, user, was_data_changed):
        delta = abs((precise_time.getTimestamp() - user.lastUpdateTimestamp) / 4)
        if delta > settings.USERS_MODULE['MAX_UPDATING_DELTA']:
            delta = settings.USERS_MODULE['MAX_UPDATING_DELTA']
        if was_data_changed:
            user.updatingPeriod -= settings.USERS_MODULE['MIN_UPDATING_DELTA']  # * 1.5
            user.updatingPeriod -= delta * 1.5
        else:
            user.updatingPeriod += settings.USERS_MODULE['MIN_UPDATING_DELTA']
            user.updatingPeriod += delta

        if user.updatingPeriod < settings.USERS_MODULE['MIN_UPDATING_PERIOD']:
            user.updatingPeriod = settings.USERS_MODULE['MIN_UPDATING_PERIOD']
        elif user.updatingPeriod > settings.USERS_MODULE['MAX_UPDATING_PERIOD']:
            user.updatingPeriod = settings.USERS_MODULE['MAX_UPDATING_PERIOD']

    def _saveModelIfLastIsNotTheSame(self, model):
        lastEntry = type(model).objects.filter(user=model.user).last()

        if lastEntry is None or int(lastEntry.value) != int(model.value):
            model.save()