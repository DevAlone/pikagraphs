from django.shortcuts import render, get_object_or_404

from communities_app.models import Community, CommunityCountersEntry

import pytz

import datetime
import time
import copy


def index(request):
    communities = Community.objects.all().order_by('-lastUpdateTimestamp')
    # for c in communities:
    #     print(c.urlName)

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


def getMoscowTimestamp(timestamp):
    return timestamp + 3600 * 3


def secret_page_for_lactarius(request):
    community = get_object_or_404(Community, urlName='leagueofartists')

    countersEntries = \
        CommunityCountersEntry.objects.filter(community=community).order_by(
            'timestamp')

    resultArray = []
    lastDay = 0
    for entry in countersEntries:
        daysSinceEpoch = (datetime.datetime.fromtimestamp(
            getMoscowTimestamp(entry.timestamp)) -
            datetime.datetime(1970, 1, 1, 3, 0)
        ).days

        if daysSinceEpoch > lastDay:
            # print('d: ' + str(daysSinceEpoch - lastDay))
            if lastDay != 0 and daysSinceEpoch - lastDay > 1:
                n = daysSinceEpoch - lastDay - 1
                for i in range(n):
                    fakeResult = copy.copy(resultArray[-1])
                    dateTime = datetime.datetime(
                        1970, 1, 1, 3, 0, 0) + datetime.timedelta(
                            lastDay + i + 1)
                    fakeResult.timestamp = time.mktime(dateTime.timetuple())
                    resultArray.append(fakeResult)

            # entry.timestamp = getMoscowTimestamp(entry.timestamp)
            resultArray.append(entry)
            lastDay = daysSinceEpoch

    for entry in resultArray:
        dt = datetime.datetime.utcfromtimestamp(entry.timestamp)
        entry.time = dt.strftime('%d.%m.%Y %H:%M')

    countersEntries = resultArray
    return render(request, 'communities_app/secret_page_for_lactarius.html', {
        'counters': countersEntries,
    })
