from django.db import models


class ScoreBoardEntry(models.Model):
    parse_timestamp = models.BigIntegerField()


class ScoreEntry(models.Model):
    username = models.CharField(max_length=50)
    avatar_url = models.CharField(max_length=128)
    score = models.IntegerField()
    date = models.CharField(max_length=64)
    scoreboard_entry = models.ForeignKey("ScoreBoardEntry", on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    __repr__ = __str__
