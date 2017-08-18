from django.shortcuts import render, get_object_or_404

from core.models import User, UserRatingEntry, UserCommentsCountEntry
from core.models import UserPostsCountEntry, UserHotPostsCountEntry
from core.models import UserPlusesCountEntry, UserMinusesCountEntry


def index(request):
    users = User.objects.all()

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

    return render(request, 'core/user.html', {
        'user': user,
        'rating': ratingEntries,
        'comments': commentsEntries,
        'posts': postsEntries,
        'hotPosts': hotPostsEntries,
        'pluses': plusesEntries,
        'minuses': minusesEntries
    })
