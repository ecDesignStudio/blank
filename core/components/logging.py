#########################################################################
#      _     ___   ____  ____ ___ _   _  ____
#     | |   / _ \ / ___|/ ___|_ _| \ | |/ ___|
#     | |  | | | | |  _| |  _ | ||  \| | |  _
#     | |__| |_| | |_| | |_| || || |\  | |_| |
#     |_____\___/ \____|\____|___|_| \_|\____|
#
#########################################################################
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'log.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
