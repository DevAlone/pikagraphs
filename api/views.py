from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from core.models import User, UserRatingEntry, UserCommentsCountEntry, UserHotPostsCountEntry, UserMinusesCountEntry, \
    UserPlusesCountEntry, UserPostsCountEntry, UserSubscribersCountEntry


def user_info(request, username):
    user = get_object_or_404(User, name=username)
    data = {
        'username': user.name,
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

    return JsonResponse(data)


def user_graph(request, username, type):
    return JsonResponse(_user_graph(username, type))


def user_graphs(request, username):
    data = {
        'ratingEntries': _user_graph(username, 'rating'),
        'commentsEntries': _user_graph(username, 'comments'),
        'postsEntries': _user_graph(username, 'posts'),
        'hotPostsEntries': _user_graph(username, 'hot_posts'),
        'minusesEntries': _user_graph(username, 'pluses'),
        'plusesEntries': _user_graph(username, 'minuses'),
        'subscribersEntries': _user_graph(username, 'subscribers'),
    }

    return JsonResponse(data)


def _user_graph(username, type):
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