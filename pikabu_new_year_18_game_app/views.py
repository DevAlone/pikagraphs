from pikabot_graphs import settings

from core.models import User, UserRatingEntry, UserCommentsCountEntry, PikabuUser, UserPostsCountEntry
from core.models import UserHotPostsCountEntry, UserPlusesCountEntry, UserMinusesCountEntry, UserSubscribersCountEntry
from communities_app.models import Community, CommunityCountersEntry
from pikabu_new_year_18_game_app.models import ScoreBoardEntry, TopItem

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import UserSerializer, CommunitySerializer, ScoreBoardEntrySerializer, PikabuUserSerializer
from core.serializers import TopItemSerializer

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

import os


class ScoreBoardViewSet(viewsets.ReadOnlyModelViewSet):
    model = ScoreBoardEntry
    queryset = ScoreBoardEntry.objects.all().order_by('-parse_timestamp')
    serializer_class = ScoreBoardEntrySerializer


class TopViewSet(viewsets.ReadOnlyModelViewSet):
    model = TopItem
    queryset = TopItem.objects.order_by('-score_entry__score').all()
    serializer_class = TopItemSerializer
