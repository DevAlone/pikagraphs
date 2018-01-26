from core.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'info', 'avatarUrl', 'rating', 'commentsCount', 'postsCount', 'hotPostsCount', 'plusesCount',
                  'minusesCount', 'lastUpdateTimestamp', 'subscribersCount', 'isRatingBan', 'updatingPeriod')
