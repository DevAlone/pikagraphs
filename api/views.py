from pikabot_graphs import settings

import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import UserSerializer, CommunitySerializer, ScoreBoardEntrySerializer, ScoreEntrySerializer

from core.models import User, UserRatingEntry, UserCommentsCountEntry
from core.models import UserPostsCountEntry, UserHotPostsCountEntry
from core.models import UserPlusesCountEntry, UserMinusesCountEntry
from core.models import UserSubscribersCountEntry

from communities_app.models import Community, CommunityCountersEntry

from pikabu_new_year_18_game_app.models import ScoreBoardEntry, ScoreEntry


def angular_debug_url(request):
    # DON'T USE IN PRODUCTION!!!

    allowed_routes = {
        '/',
        '/inline.bundle.js',
        '/polyfills.bundle.js',
        '/styles.bundle.js',
        '/vendor.bundle.js',
        '/main.bundle.js'
    }
    routes = {
        '/': '/index.html'
    }

    if request.path not in allowed_routes:
        request.path = '/'

    route = routes[request.path] if request.path in routes else request.path
    route = route[1:]

    file_path = os.path.join(settings.ANGULAR_ROOT, route)
    try:
        with open(file_path, 'r') as file:
            return HttpResponse(file.read())
    except:
        pass

    request.path = '/'
    return angular_debug_url(request)


class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    model = None
    sort_by_fields = []
    filter_by_fields = []

    def get_queryset(self):
        params = self.request.query_params

        search_text = params['search_text'].lower() if 'search_text' in params else ''

        queryset = self.model.objects

        if self.sort_by_fields:
            sort_by_field = params['sort_by'].lower() if 'sort_by' in params else ''

            if sort_by_field not in self.sort_by_fields:
                sort_by_field = self.sort_by_fields[0]

            reverse_sort = params['reverse_sort'].lower() if 'reverse_sort' in params else 'false'
            reverse_sort = reverse_sort == 'true'

            queryset = queryset.order_by(('-' if reverse_sort else '') + sort_by_field)

        if search_text:
            # filter_object = Q(name__contains=search_text) | Q(url_name=search_text)
            filter_object = None
            for filter_field in self.filter_by_fields:
                if filter_object is None:
                    filter_object = Q(**{filter_field + '__contains': search_text})
                else:
                    filter_object |= Q(**{filter_field + '__contains': search_text})

            if filter_object is not None:
                queryset = queryset.filter(filter_object)

        return queryset.all()


class UserViewSet(SearchViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    sort_by_fields = [
        'rating',
        'username',
        'subscribers_count',
        'comments_count',
        'posts_count',
        'hot_posts_count',
        'pluses_count',
        'minuses_count',
        'next_updating_timestamp',
        'updating_period',
    ]
    filter_by_fields = ['username', 'info']


@api_view(['GET'])
def get_user_graph(request, username, graph_name):
    user = get_object_or_404(User, username=username)
    graph_name = graph_name.lower()

    classes = {
        'rating': UserRatingEntry,
        'comments': UserCommentsCountEntry,
        'posts': UserPostsCountEntry,
        'hot_posts': UserHotPostsCountEntry,
        'pluses': UserPlusesCountEntry,
        'minuses': UserMinusesCountEntry,
        'subscribers': UserSubscribersCountEntry,
    }

    if graph_name not in classes:
        return HttpResponse(status=404)

    data = classes[graph_name].objects.filter(user=user).order_by('timestamp').all()

    data = [
        {
            'timestamp': item.timestamp,
            'value': item.value,
            # 'user_id',
        } for item in data
    ]

    return Response({
        'results': data
    })


class UserView(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommunityViewSet(SearchViewSet):
    model = Community
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    sort_by_fields = [
        'subscribers_count',
        'name',
        'stories_count',
        'last_update_timestamp',
    ]
    filter_by_fields = ['url_name', 'name', 'description']


@api_view(['GET'])
def get_community_graph(request, url_name, graph_name):
    community = get_object_or_404(Community, url_name=url_name)

    graph_name = graph_name.lower()

    classes = {
        'subscribers': CommunityCountersEntry,
        'stories': CommunityCountersEntry,
    }

    if graph_name not in classes:
        return HttpResponse(status=404)

    data = classes[graph_name].objects.filter(community=community).order_by('timestamp').all()

    data = [
        {
            'timestamp': item.timestamp,
            'value': item.subscribers_count if graph_name == 'subscribers' else item.stories_count,
            # 'user_id',
        } for item in data
    ]

    return Response({
        'results': data
    })


class CommunityView(generics.RetrieveAPIView):
    lookup_field = 'url_name'
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class ScoreBoardViewSet(viewsets.ReadOnlyModelViewSet):
    model = ScoreBoardEntry
    queryset = ScoreBoardEntry.objects.all().order_by('-parse_timestamp')
    serializer_class = ScoreBoardEntrySerializer


class TopViewSet(viewsets.ReadOnlyModelViewSet):
    model = ScoreEntry
    queryset = ScoreEntry.objects.all().order_by('-score')
    serializer_class = ScoreEntrySerializer
