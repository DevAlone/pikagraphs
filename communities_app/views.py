from django.shortcuts import render, get_object_or_404

from communities_app.models import Community, CommunityCountersEntry

import datetime


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
