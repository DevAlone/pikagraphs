from django.db import models


class Community(models.Model):
    urlName = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, default="")
    subscribersCount = models.IntegerField(default=0)
    storiesCount = models.IntegerField(default=0)
    lastUpdateTimestamp = models.BigIntegerField(default=0)

    class Meta:
        db_table = "community"

    def __str__(self):
        return self.name

    __repr__ = __str__


class CommunityCountersEntry(models.Model):
    timestamp = models.BigIntegerField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    subscribersCount = models.IntegerField(default=0)
    storiesCount = models.IntegerField(default=0)

    def __str__(self):
        return self.community.name

    __repr__ = __str__
