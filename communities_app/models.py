from django.db import models


class Community(models.Model):
    objects = None

    url_name = models.CharField(max_length=64, unique=True)
    name = models.TextField(default="", db_index=True)
    description = models.TextField(null=True)
    avatar_url = models.URLField(default="")
    background_image_url = models.URLField(default="")
    subscribers_count = models.IntegerField(default=0, db_index=True)
    stories_count = models.IntegerField(default=0, db_index=True)
    last_update_timestamp = models.BigIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name

    __repr__ = __str__


class CommunityCountersEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    subscribers_count = models.IntegerField(default=0)
    stories_count = models.IntegerField(default=0)

    def __str__(self):
        return self.community.name

    __repr__ = __str__
