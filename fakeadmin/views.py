from django.shortcuts import render


def fakeAdmin(request):
    return render(request, 'fakeadmin/fakeAdmin.html')
