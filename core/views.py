from pikabot_graphs import settings

import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import views
from rest_framework import viewsets
from rest_framework.decorators import api_view
from core.serializers import UserSerializer

from core.models import User, UserRatingEntry, UserCommentsCountEntry
from core.models import UserPostsCountEntry, UserHotPostsCountEntry
from core.models import UserPlusesCountEntry, UserMinusesCountEntry
from core.models import UserSubscribersCountEntry

#
# def index(request):
#     users = User.objects.all().order_by('-rating')[:5]  # .order_by('-lastUpdateTimestamp')
#     graphs = []
#     for user in users:
#         graph = {
#             'user': user,
#             'points': UserRatingEntry.objects.filter(user=user).order_by('timestamp'),
#         }
#         graphs.append(graph)
#         # for entry in UserRatingEntry.objects.filter(user=user).order_by('timestamp'):
#         #     graph['points'].append(entry)
#
#     return render(request, 'core/index.html', {
#         'users': users,
#         'graphs': graphs,
#     })
#
#
# def users(request):
#     users = User.objects.all()  # .order_by('-lastUpdateTimestamp')
#
#     return render(request, 'core/users.html', {
#         'users': users,
#     })
#
#
# def user(request, username):
#     username = username.lower()
#     user = get_object_or_404(User, name=username)
#
#     rating_entries = \
#         UserRatingEntry.objects.filter(user=user).order_by('timestamp')
#     comments_entries = \
#         UserCommentsCountEntry.objects.filter(user=user).order_by('timestamp')
#     posts_entries = \
#         UserPostsCountEntry.objects.filter(user=user).order_by('timestamp')
#     hot_posts_entries = \
#         UserHotPostsCountEntry.objects.filter(user=user).order_by('timestamp')
#     pluses_entries = \
#         UserPlusesCountEntry.objects.filter(user=user).order_by('timestamp')
#     minuses_entries = \
#         UserMinusesCountEntry.objects.filter(user=user).order_by('timestamp')
#     subscribers_entries = \
#         UserSubscribersCountEntry.objects.filter(user=user)\
#         .order_by('timestamp')
#
#     return render(request, 'core/user.html', {
#         'user': user,
#         'rating': rating_entries,
#         'comments': comments_entries,
#         'posts': posts_entries,
#         'hotPosts': hot_posts_entries,
#         'pluses': pluses_entries,
#         'minuses': minuses_entries,
#         'subscribers': subscribers_entries,
#     })


def secret_page_for_l4rever(request):
    users = User.objects.all().order_by('-subscribers_count')
    return render(request, 'core/secret_page_for_l4rever.html', {
        'users': users,
    })


def ok(request):
    return HttpResponse("OK")

# REST

