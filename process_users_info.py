import bot.init_django_models

from core.models import User, PikabuUser
from bot.users_module import UsersModule
import json
import sys
import logging


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""USAGE
        {} DATABASE_FILE
        """.format(sys.argv[0]))
        exit(1)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(log_handler)

    with open(sys.argv[1], 'r') as file:
        for line in file:
            json_data = json.loads(line.strip())
            json_data = json_data['user']

            logger.info('start processing {}'.format(json_data['user_name']))

            username = json_data['user_name'].strip().lower()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User()
                user.username = username

            UsersModule._update_user(user, json_data, logger)
            user.save()

            pikabu_user = PikabuUser.objects.get(username=json_data['user_name'])
            pikabu_user.is_processed = True
            pikabu_user.save()
