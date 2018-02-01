import bot.init_django_models

from pikabu_new_year_18_game_app.models import ScoreBoardEntry, ScoreEntry, TopItem


if __name__ == '__main__':
    TopItem.objects.all().delete()

    usernames = set()

    for entry in ScoreEntry.objects.order_by('-score').all():
        if entry.username not in usernames:
            TopItem(score_entry=entry).save()
            usernames.add(entry.username)
