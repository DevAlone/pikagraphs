from django.db import models


class User(models.Model):
    # to disable pycharm's attribute checking
    objects = None
    DoesNotExist = None

    pikabu_id = models.BigIntegerField(null=True)

    username = models.CharField(max_length=64, unique=True)
    avatar_url = models.TextField(default="")
    rating = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    hot_posts_count = models.IntegerField(default=0)
    pluses_count = models.IntegerField(default=0)
    minuses_count = models.IntegerField(default=0)
    subscribers_count = models.IntegerField(default=0)
    is_rating_ban = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, default='-')
    approved = models.TextField(default="")
    awards = models.TextField(default="")
    communities = models.TextField(default="")
    signup_timestamp = models.IntegerField(default=0)

    info = models.TextField(blank=True, null=True)

    updating_period = models.IntegerField(default=60)
    is_updated = models.BooleanField(default=False)

    last_update_timestamp = models.IntegerField(default=0, db_index=True)

    @property
    def next_update_timestamp(self):
        return self.last_update_timestamp + self.updating_period

    def __str__(self):
        return self.username

    __repr__ = __str__

    class Meta:
        permissions = (
            ("edit_info_field", "Can edit info field"),
        )


class UserRatingEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserCommentsCountEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserPostsCountEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserHotPostsCountEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserPlusesCountEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserMinusesCountEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserSubscribersCountEntry(models.Model):
    objects = None

    timestamp = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class PikabuUser(models.Model):
    objects = None
    DoesNotExist = None

    pikabu_id = models.BigIntegerField(primary_key=True)
    username = models.TextField()
    is_processed = models.BooleanField(default=False)
