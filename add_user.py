import sys
import re

import bot.init_django_models

from core.models import User


def add_user_by_username(username: str):
    username = username.lower().strip()

    if not re.match(r'^[a-z0-9._]+$', username):
        print('bad username')
        raise Exception()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print('creating {}...'.format(username))
        user = User()
        user.username = username

    if not user.is_updated:
        print('setting is_updated field to True...')
        user.is_updated = True

    user.save()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""USAGE:
        python3 {} username
        """.format(sys.argv[0]))
        exit(1)

    add_user_by_username(sys.argv[1])
