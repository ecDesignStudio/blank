"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from split_settings.tools import optional, include

include(
    'components/base.py',
    'components/database.py',
    'components/email.py',
    'components/logging.py',
    'components/i18n.py',
    'components/thirdparty.py',
    optional('settings_local.py')
)