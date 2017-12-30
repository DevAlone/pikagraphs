from django.shortcuts import render
from django.http import JsonResponse

from .models import ScoreEntry, ScoreBoardEntry


def index(request):
    return render(request, "pikabu_new_year_18_game_app/index.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })


def avatars_only(request):
    return render(request, "pikabu_new_year_18_game_app/avatars_only.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })


def ugly_frontend(request):
    return render(request, "pikabu_new_year_18_game_app/ugly_frontend.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })


def get_score_items(request, from_timestamp, to_timestamp):
    scoreboards = []

    for score_board_entry in ScoreBoardEntry.objects.filter(parse_timestamp__gte=from_timestamp).filter(
            parse_timestamp__lte=to_timestamp).order_by('-parse_timestamp'):
        items = [
            {
                "username": score_entry.username,
                "avatar_url": score_entry.avatar_url,
                "score": score_entry.score,
                "date": score_entry.date,
            } for score_entry in score_board_entry.scoreentry_set.order_by('-score')
        ]
        scoreboard = {
            "items": items,
        }
        scoreboards.append(scoreboard)

    return JsonResponse({
        'scoreboards': scoreboards,
    })