from pikabot_graphs import settings

import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework import generics
from rest_framework import viewsets
from core.serializers import UserSerializer

from core.models import User, UserRatingEntry, UserCommentsCountEntry
from core.models import UserPostsCountEntry, UserHotPostsCountEntry
from core.models import UserPlusesCountEntry, UserMinusesCountEntry
from core.models import UserSubscribersCountEntry


def index(request):
    users = User.objects.all().order_by('-rating')[:5]  # .order_by('-lastUpdateTimestamp')
    graphs = []
    for user in users:
        graph = {
            'user': user,
            'points': UserRatingEntry.objects.filter(user=user).order_by('timestamp'),
        }
        graphs.append(graph)
        # for entry in UserRatingEntry.objects.filter(user=user).order_by('timestamp'):
        #     graph['points'].append(entry)

    return render(request, 'core/index.html', {
        'users': users,
        'graphs': graphs,
    })


def users(request):
    users = User.objects.all()  # .order_by('-lastUpdateTimestamp')

    return render(request, 'core/users.html', {
        'users': users,
    })


def user(request, username):
    username = username.lower()
    user = get_object_or_404(User, name=username)

    ratingEntries = \
        UserRatingEntry.objects.filter(user=user).order_by('timestamp')
    commentsEntries = \
        UserCommentsCountEntry.objects.filter(user=user).order_by('timestamp')
    postsEntries = \
        UserPostsCountEntry.objects.filter(user=user).order_by('timestamp')
    hotPostsEntries = \
        UserHotPostsCountEntry.objects.filter(user=user).order_by('timestamp')
    plusesEntries = \
        UserPlusesCountEntry.objects.filter(user=user).order_by('timestamp')
    minusesEntries = \
        UserMinusesCountEntry.objects.filter(user=user).order_by('timestamp')
    subscribersEntries = \
        UserSubscribersCountEntry.objects.filter(user=user)\
        .order_by('timestamp')

    return render(request, 'core/user.html', {
        'user': user,
        'rating': ratingEntries,
        'comments': commentsEntries,
        'posts': postsEntries,
        'hotPosts': hotPostsEntries,
        'pluses': plusesEntries,
        'minuses': minusesEntries,
        'subscribers': subscribersEntries,
    })


def secret_page_for_l4rever(request):
    users = User.objects.all().order_by('-subscribersCount')
    return render(request, 'core/secret_page_for_l4rever.html', {
        'users': users,
    })


def OK(request):
    return HttpResponse("OK")

# REST


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    model = User
    queryset = User.objects.all().order_by('-rating')
    serializer_class = UserSerializer

# class UserViewSet(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


def angular_debug_url(request):
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

    if request.path in allowed_routes:
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
    # return HttpResponse("Not found1", status=404)
