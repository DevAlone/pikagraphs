from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from core.models import User, UserRatingEntry, UserCommentsCountEntry, UserHotPostsCountEntry, UserMinusesCountEntry, \
    UserPlusesCountEntry, UserPostsCountEntry, UserSubscribersCountEntry
from communities_app.models import Community, CommunityCountersEntry

import json


def users(request):
    limit = int(request.GET.get('limit', 10))
    if limit < 1 or limit > 100:
        limit = 10

    offset = int(request.GET.get('offset', 0))
    if offset < 0:
        offset = 0

    search_text = request.GET.get('search', "").lower()
    sort_by_field = request.GET.get('sort_by', "")

    if sort_by_field not in [
        'rating',
        'subscribersCount',
    ]:
        sort_by_field = 'rating'

    reverse_sort = request.GET.get('reverse_sort', "true").lower()

    users = User.objects.all().order_by(('-' if reverse_sort == "true" else '') + sort_by_field)

    if search_text:
        users = users.filter(name__contains=search_text)

    users = users[offset : offset + limit]

    return JsonResponse({
        'hasMore': bool(users),
        'data': [serialize_user(user) for user in users],
        'sortedByField': sort_by_field,
    })


def user_info(request, username):
    username = username.lower()
    user = get_object_or_404(User, name=username)

    return JsonResponse(serialize_user(user))


def edit_user_info_field(request, username):
    if not request.user.is_authenticated() or not request.user.has_perm('core.edit_info_field'):
        return JsonResponse({
            'error': "You don't have permissions to do that",
        })

    if request.method == 'POST' and request.is_ajax():
        data = request.body.decode('utf8')
        user = get_object_or_404(User, name=username)
        user.info = data
        user.save()

        return JsonResponse({
            'status': 'ok',
            'info': user.info,
        })

    return JsonResponse({
        'error': 'Something went wrong',
    })


def community_info(request, urlName):
    urlName = urlName.lower()
    community = get_object_or_404(Community, urlName=urlName)

    return JsonResponse({
        'urlName': community.urlName,
        'name': community.name,
        'subscribersCount': community.subscribersCount,
        'storiesCount': community.storiesCount,
        'lastUpdateTimestamp': community.lastUpdateTimestamp,
    })


def user_graph(request, username, type):
    return JsonResponse(_user_graph(username, type))


def user_graphs(request, username):
    return JsonResponse({
        'ratingEntries': _user_graph(username, 'rating'),
        'commentsEntries': _user_graph(username, 'comments'),
        'postsEntries': _user_graph(username, 'posts'),
        'hotPostsEntries': _user_graph(username, 'hot_posts'),
        'minusesEntries': _user_graph(username, 'pluses'),
        'plusesEntries': _user_graph(username, 'minuses'),
        'subscribersEntries': _user_graph(username, 'subscribers'),
    })


def _user_graph(username, type):
    username = username.lower()
    user = get_object_or_404(User, name=username)
    Type = {
        'rating': UserRatingEntry,
        'comments': UserCommentsCountEntry,
        'posts': UserPostsCountEntry,
        'hot_posts': UserHotPostsCountEntry,
        'pluses': UserPlusesCountEntry,
        'minuses': UserMinusesCountEntry,
        'subscribers': UserSubscribersCountEntry,
    }[type]

    data = {
        'items': [
            {
                'timestamp': item.timestamp,
                'value': item.value
            } for item in Type.objects.filter(user=user)]
    }

    return data


def community_graphs(request, urlName):
    urlName = urlName.lower()
    community = get_object_or_404(Community, urlName=urlName)

    return JsonResponse({
        'items': [
            {
                'timestamp': item.timestamp,
                'subscribersCount': item.subscribersCount,
                'storiesCount': item.storiesCount,
            } for item in CommunityCountersEntry.objects.filter(community=community)]
    })


def serialize_user(user : User):
    return {
        'username': user.name,
        'avatarUrl': user.avatarUrl,
        'info': user.info,
        'rating': user.rating,
        'commentsCount': user.commentsCount,
        'postsCount': user.postsCount,
        'hotPostsCount': user.hotPostsCount,
        'plusesCount': user.plusesCount,
        'minusesCount': user.minusesCount,
        'subscribersCount': user.subscribersCount,
        'lastUpdateTimestamp': user.lastUpdateTimestamp,
        'isRatingBan': user.isRatingBan,
        'updatingPeriod': user.updatingPeriod,
    }