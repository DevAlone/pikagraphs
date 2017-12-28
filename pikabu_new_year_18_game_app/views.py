from django.shortcuts import render

from .models import ScoreEntry, ScoreBoardEntry


def index(request):
    return ugly_frontend(request)


def ugly_frontend(request):
    return render(request, "pikabu_new_year_18_game_app/ugly_frontend.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })