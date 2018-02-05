from communities_app.models import Community, CommunityCountersEntry

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import CommunitySerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend  # , FilterSet

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


# API

# class CommunityFilter(FilterSet):
#     class Meta:
#         model = Community
#         fields = {
#             'pikabu_id': ('exact', 'lte', 'gte'),
#             'username': ('exact', 'contains', 'icontains'),
#             'is_processed': ('exact', )
#         }


class CommunityViewSet(viewsets.ReadOnlyModelViewSet):
    model = Community
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = (
        'subscribers_count',
        'name',
        'stories_count',
        'last_update_timestamp',
    )
    ordering = ('pk',)
    search_fields = ('url_name', 'name', 'description', )
    # filter_class = UserFilter


@api_view(['GET'])
def get_community_graph(_, url_name, graph_name):
    community = get_object_or_404(Community, url_name=url_name)

    graph_name = graph_name.lower()

    classes = {
        'subscribers': CommunityCountersEntry,
        'stories': CommunityCountersEntry,
    }

    if graph_name not in classes:
        return HttpResponse(status=404)

    data = classes[graph_name].objects.filter(community=community).order_by('pk').all()

    data = [
        {
            'timestamp': item.timestamp,
            'value': item.subscribers_count if graph_name == 'subscribers' else item.stories_count,
            # 'user_id',
        } for item in data
    ]

    return Response({
        'results': data
    })


class CommunityView(generics.RetrieveAPIView):
    lookup_field = 'url_name'
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
