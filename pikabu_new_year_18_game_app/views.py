import datetime
import time

from django.shortcuts import render
from django.http import JsonResponse

from .models import ScoreEntry, ScoreBoardEntry


def memoization(seconds):
    def decorator(function):
        setattr(function, "_last_processing_time", 0)
        setattr(function, "_last_return_obj", None)
        def wrapper(*args, **kwargs):
            if function._last_return_obj is None or function._last_processing_time + seconds < time.time():
                function._last_return_obj = function(*args, **kwargs)
                function._last_processing_time = time.time()

            return function._last_return_obj

        return wrapper

    return decorator


def index(request):
    return render(request, "pikabu_new_year_18_game_app/index.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })


def avatars_only(request):
    return render(request, "pikabu_new_year_18_game_app/avatars_only.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })


@memoization(60)
def top(request):
    # entries_by_score = ScoreEntry.objects.order_by("-score").distinct("username", "score")
    entries_by_score = []
    for entry in ScoreEntry.objects.order_by("-score"):
        if not entries_by_score or not (
                entries_by_score[-1].username == entry.username and entries_by_score[-1].score == entry.score):
            entries_by_score.append(entry)

    return render(request, "pikabu_new_year_18_game_app/top.html", {
        "entries": entries_by_score,
    })


@memoization(5 * 60)
def top_by_time_in_scoreboard(request):
    def score_items_has_user(score_items: list, username: str):
        for item in score_items:
            if item.username == username:
                return True

        return False

    users = {}

    previous_score_items = None

    for scoreboard in ScoreBoardEntry.objects.order_by("parse_timestamp"):
        score_items = scoreboard.scoreentry_set.all()
        for score_item in score_items:
            if score_item.username not in users:
                users[score_item.username] = {
                    "avatar_url": score_item.avatar_url,
                    "maximum_range": 60,
                    "first_timestamp": scoreboard.parse_timestamp,
                    "last_timestamp": scoreboard.parse_timestamp,
                }
            elif score_items_has_user(previous_score_items, score_item.username):
                users[score_item.username]["last_timestamp"] = scoreboard.parse_timestamp
                range = \
                    users[score_item.username]["last_timestamp"] - users[score_item.username]["first_timestamp"] + 60
                if range > users[score_item.username]["maximum_range"]:
                    users[score_item.username]["maximum_range"] = range
                    users[score_item.username]["avatar_url"] = score_item.avatar_url
            else:
                users[score_item.username]["last_timestamp"] = scoreboard.parse_timestamp
                users[score_item.username]["first_timestamp"] = scoreboard.parse_timestamp

        previous_score_items = score_items

    entries = []

    for key, value in users.items():
        entries.append({
            "username": key,
            "avatar_url": value["avatar_url"],
            "maximum_time": datetime.timedelta(seconds=value["maximum_range"]),
        })

    entries.sort(key=lambda x: -x["maximum_time"])

    return render(request, "pikabu_new_year_18_game_app/top_by_time_in_scoreboard.html", {
        "entries": entries,
    })


def ugly_frontend(request):
    return render(request, "pikabu_new_year_18_game_app/ugly_frontend.html", {
        'score_boards': list(ScoreBoardEntry.objects.order_by("-parse_timestamp"))
    })


def get_score_items(request, from_timestamp, to_timestamp):
    def areScoreboardsEqual(first, second):
        if len(first["items"]) != len(second["items"]):
            return False

        for i in range(len(first["items"])):
            first_item = first["items"][i]
            second_item = second["items"][i]
            if first_item["username"] != second_item["username"] or \
                    first_item["avatar_url"] != second_item["avatar_url"] or \
                    first_item["score"] != second_item["score"]:
                return False

        return True

    scoreboards = []

    previousScoreboard = None

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
            "parse_timestamp": score_board_entry.parse_timestamp,
        }
        if previousScoreboard is None or not areScoreboardsEqual(previousScoreboard, scoreboard):
            scoreboards.append(scoreboard)

        previousScoreboard = scoreboard

    return JsonResponse({
        'scoreboards': scoreboards,
    })