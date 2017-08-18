from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rating = models.IntegerField(default=0)
    commentsCount = models.IntegerField(default=0)
    postsCount = models.IntegerField(default=0)
    hotPostsCount = models.IntegerField(default=0)
    plusesCount = models.IntegerField(default=0)
    minusesCount = models.IntegerField(default=0)
    lastUpdateTimestamp = models.BigIntegerField(default=0)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name

    __repr__ = __str__


class UserRatingEntry(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserCommentsCountEntry(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserPostsCountEntry(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserHotPostsCountEntry(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserPlusesCountEntry(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__


class UserMinusesCountEntry(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.user.name

    __repr__ = __str__
