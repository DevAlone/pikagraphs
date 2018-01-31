from core.models import User
from communities_app.models import Community
from pikabu_new_year_18_game_app.models import ScoreBoardEntry, ScoreEntry
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'info', 'avatar_url', 'rating', 'comments_count', 'posts_count', 'hot_posts_count',
                  'pluses_count', 'minuses_count', 'last_update_timestamp', 'next_updating_timestamp',
                  'subscribers_count', 'is_rating_ban', 'updating_period', 'is_updated')


class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Community
        fields = ('url_name', 'name', 'description', 'avatar_url', 'background_image_url', 'subscribers_count',
                  'stories_count', 'last_update_timestamp')


class ScoreEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoreEntry
        fields = ('username', 'avatar_url', 'score', 'date')


class ScoreBoardEntrySerializer(serializers.HyperlinkedModelSerializer):
    score_entries = ScoreEntrySerializer(many=True, read_only=True)

    class Meta:
        model = ScoreBoardEntry
        fields = ('parse_timestamp', 'score_entries')
