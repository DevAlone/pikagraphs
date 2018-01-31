from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    info = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(default="https://cs.pikabu.ru/images/def_avatar/def_avatar_96.png")
    rating = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    hot_posts_count = models.IntegerField(default=0)
    pluses_count = models.IntegerField(default=0)
    minuses_count = models.IntegerField(default=0)
    last_update_timestamp = models.BigIntegerField(default=0, db_index=True)
    subscribers_count = models.IntegerField(default=0)
    is_rating_ban = models.BooleanField(default=False)
    updating_period = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    __repr__ = __str__

    class Meta:
        permissions = (
            ("edit_info_field", "Can edit info field"),
        )


class UserRatingEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserCommentsCountEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserPostsCountEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserHotPostsCountEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserPlusesCountEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserMinusesCountEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserSubscribersCountEntry(models.Model):
    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__
