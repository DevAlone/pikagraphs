from django.shortcuts import render, get_object_or_404

from communities_app.models import Community, CommunityCountersEntry

import datetime
# import time
# import copy


def index(request):
    communities = Community.objects.all().order_by('-lastUpdateTimestamp')
    # for c in communities:
    #     print(c.urlName)

    return render(request, 'communities_app/index.html', {
        'communities': communities,
    })


def community(request, url_name):
    url_name = url_name.lower()
    community = get_object_or_404(Community, urlName=url_name)

    counters_entries = \
        CommunityCountersEntry.objects.filter(community=community).order_by(
            'timestamp')

    return render(request, 'communities_app/community.html', {
        'community': community,
        'counters': counters_entries,
    })


def get_moscow_timestamp(timestamp):
    return timestamp + 3600 * 3


def secret_page_for_lactarius(request):
    community = get_object_or_404(Community, url_name='leagueofartists')

    counters_entries = \
        CommunityCountersEntry.objects.filter(community=community).order_by(
            'timestamp')

    result_array = []
    last_day = 0
    for entry in counters_entries:
        days_since_epoch = (datetime.datetime.utcfromtimestamp(
            get_moscow_timestamp(entry.timestamp)) -
                          datetime.datetime.utcfromtimestamp(0)
                          ).days

        if days_since_epoch > last_day:
            # if lastDay != 0 and daysSinceEpoch - lastDay > 1:
            #     n = daysSinceEpoch - lastDay - 1
            #     for i in range(n):
            #         fakeResult = copy.copy(resultArray[-1])
            #         dateTime = datetime.datetime(
            #            1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc) + \
            #            datetime.timedelta(
            #                lastDay + i + 1)
            #        fakeResult.timestamp = time.mktime(dateTime.timetuple())
            #        resultArray.append(fakeResult)

            entry.timestamp = get_moscow_timestamp(entry.timestamp)
            result_array.append(entry)
            last_day = days_since_epoch

    for entry in result_array:
        dt = datetime.datetime.utcfromtimestamp(entry.timestamp)
        entry.time = dt.strftime('%d.%m.%Y %H:%M')

    counters_entries = result_array
    return render(request, 'communities_app/secret_page_for_lactarius.html', {
        'counters': counters_entries,
    })
