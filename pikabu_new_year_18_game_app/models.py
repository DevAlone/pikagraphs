from django.db import models


class ScoreBoardEntry(models.Model):
    objects = None

    parse_timestamp = models.BigIntegerField()


class ScoreEntry(models.Model):
    objects = None

    username = models.CharField(max_length=50)
    avatar_url = models.CharField(max_length=128)
    score = models.IntegerField()
    date = models.CharField(max_length=64)
    scoreboard_entry = models.ForeignKey("ScoreBoardEntry", related_name='score_entries', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    __repr__ = __str__

    class Meta:
        ordering = ['score']


class TopItem(models.Model):
    objects = None

    score_entry = models.OneToOneField(ScoreEntry, on_delete=models.CASCADE, primary_key=True)
