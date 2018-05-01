import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Bot settings

USERS_MODULE = {
    'MIN_UPDATING_PERIOD': 3600 * 12,
    'MAX_UPDATING_PERIOD': 3600 * 24 * 15,
    'MIN_UPDATING_DELTA': 60,
    'MAX_UPDATING_DELTA': 3600 * 24 * 2,
    'RESTORE_UPDATING_PERIOD_COEFFICIENT': 3,
    'PROCESSING_ON_RATING': 0,
    'PROCESSING_ON_SUBSCRIBERS_COUNT': 0,
    'PROCESSING_ON_APPROVED': True,
    'UPDATING_PERIOD': 30,
}

COMMUNITIES_MODULE = 
    'UPDATING_PERIOD': 1 * 3600
}

BOT_CONCURRENT_TASKS = 256
BOT_CLIENT_TIMEOUT = 10

PARSE_ALL_USERS_MODULE = {
    'PROCESSING_PERIOD': 60,
    'PROCESSING_GAP_SIZE': 10,
    'PROCESSING_CYCLES': 1,
    'USERNAME': None,
    'PASSWORD': None,
}

# / Bot settings

ALLOWED_PUSH_USERS_SESSIONS = []
ALLOWED_USERS_SESSIONS = []

API_SERVER_ADDRESS = '127.0.0.1'
