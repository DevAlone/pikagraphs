import sys
import re

import bot.init_django_models

from core.models import User


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""USAGE:
        python3 {} username
        """.format(sys.argv[0]))
        exit(1)

    username = sys.argv[1].lower().strip()

    if not re.match(r'^[a-z0-9._]+$', username):
        print('bad username')
        exit(2)

    user, was_created = User.objects.get_or_create(username=username)
    if not user.is_updated:
        if was_created:
            print('creating {}...'.format(user.username))

        print('setting is_updated field to True...')
        user.is_updated = True
        user.save()
