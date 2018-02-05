from pikabot_graphs import settings
from core.models import User, UserRatingEntry, UserCommentsCountEntry, PikabuUser, UserPostsCountEntry
from core.models import UserHotPostsCountEntry, UserPlusesCountEntry, UserMinusesCountEntry, UserSubscribersCountEntry

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import UserSerializer, PikabuUserSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

import os


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
    except FileNotFoundError:
        pass

    request.path = '/'
    return angular_debug_url(request)


def secret_page_for_l4rever(request):
    users = User.objects.all().order_by('-subscribers_count')
    return render(request, 'core/secret_page_for_l4rever.html', {
        'users': users,
    })


def ok(_):
    return HttpResponse("OK")


# API


# class UserFilter(FilterSet):
#     class Meta:
#         model = User
#         fields = {
#             'pikabu_id': ('exact', 'lte', 'gte'),
#             'username': ('exact', 'contains', 'icontains'),
#             'is_processed': ('exact', )
#         }


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = (
        'rating',
        'username',
        'subscribers_count',
        'comments_count',
        'posts_count',
        'hot_posts_count',
        'pluses_count',
        'minuses_count',
        'last_update_timestamp',
        'updating_period',
        'pikabu_id',
        'approved',
        'signup_timestamp',
        'pk',
    )
    ordering = ('pk',)
    search_fields = ('username', 'info', 'approved', )
    # filter_class = UserFilter


@api_view(['GET'])
def get_user_graph(_, username, graph_name):

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


class PikabuUserFilter(FilterSet):
    class Meta:
        model = PikabuUser
        fields = {
            'pikabu_id': ('exact', 'lte', 'gte'),
            'username': ('exact', 'contains', 'icontains'),
            'is_processed': ('exact', )
        }


class PikabuUserViewSet(viewsets.ReadOnlyModelViewSet):
    model = PikabuUser
    queryset = PikabuUser.objects.all()
    serializer_class = PikabuUserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('pikabu_id', 'username')
    ordering = ('pikabu_id',)
    filter_class = PikabuUserFilter
