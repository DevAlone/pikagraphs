import bot.init_django_models

from pikabu_new_year_18_game_app.models import ScoreBoardEntry, ScoreEntry


def are_scoreboards_equal(scoreboard1: ScoreBoardEntry, scoreboard2: ScoreBoardEntry) -> bool:
    items1 = scoreboard1.score_entries.all()
    items2 = scoreboard2.score_entries.all()

    if len(items1) != len(items2):
        return False

    for i in range(len(items1)):
        item1 = items1[i]
        item2 = items2[i]

        if item1.username != item2.username or item1.avatar_url != item2.avatar_url or item1.score != item2.score\
                or item1.date != item2.date:
            return False

    return True


if __name__ == '__main__':
    scoreboards = ScoreBoardEntry.objects.order_by('parse_timestamp').all()

    previous_score_board = None

    items_count = 0
    deleted_count = 0

    for scoreboard in scoreboards:
        items_count += 1
        if previous_score_board is not None:
            if are_scoreboards_equal(previous_score_board, scoreboard):
                deleted_count += 1
                scoreboard.delete()
            else:
                previous_score_board = scoreboard

    print('items: {}\ndeleted: {}'.format(items_count, deleted_count))
