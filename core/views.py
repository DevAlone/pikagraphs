from django.shortcuts import render
from django.http import HttpResponse

from core.models import User


def secret_page_for_l4rever(request):
    users = User.objects.all().order_by('-subscribers_count')
    return render(request, 'core/secret_page_for_l4rever.html', {
        'users': users,
    })


def ok(request):
    return HttpResponse("OK")
