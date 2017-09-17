from django.shortcuts import render, get_object_or_404

from communities_app.models import Community, CommunityCountersEntry


def index(request):
    communities = Community.objects.all().order_by('-lastUpdateTimestamp')
    for c in communities:
        print(c.urlName)

    return render(request, 'communities_app/index.html', {
        'communities': communities,
    })


def community(request, urlName):
    urlName = urlName.lower()
    community = get_object_or_404(Community, urlName=urlName)

    countersEntries = \
        CommunityCountersEntry.objects.filter(community=community).order_by(
            'timestamp')

    return render(request, 'communities_app/community.html', {
        'community': community,
        'counters': countersEntries,
    })


def secret_page_for_lactarius(request):
    community = get_object_or_404(Community, urlName='leagueofartists')

    countersEntries = \
        CommunityCountersEntry.objects.filter(community=community).order_by(
            'timestamp')

    return render(request, 'communities_app/secret_page_for_lactarius.html', {
        'counters': countersEntries,
    })
