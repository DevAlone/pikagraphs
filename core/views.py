from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from core.models import User, UserRatingEntry, UserCommentsCountEntry
from core.models import UserPostsCountEntry, UserHotPostsCountEntry
from core.models import UserPlusesCountEntry, UserMinusesCountEntry
from core.models import UserSubscribersCountEntry


def index(request):
    users = User.objects.all().order_by('-lastUpdateTimestamp')

    return render(request, 'core/index.html', {
        'users': users,
    })


def user(request, username):
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
