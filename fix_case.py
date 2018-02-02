import bot.init_django_models

from core.models import PikabuUser, User

import string


if __name__ == '__main__':
    for letter in string.ascii_uppercase:
        print('checking {}'.format(letter))
        users = User.objects.filter(username__contains=letter).all()

        for user in filter(lambda user: letter in user.username, users):
            username = user.username.strip().lower()
            print('before "{}" after "{}"'.format(user.username, username))

            try:
                User.objects.get(username=username)
                user.delete()
                print('exists')
            except User.DoesNotExist:
                print('not exists')
                user.username = username
                user.save()

        print('\n')
