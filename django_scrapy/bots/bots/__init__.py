#!/usr/bin/env python
# -*- coding:utf-8 -*-


def setup_django_env():
    import os
    import sys
    import django

    sys.path.append('/Users/zyx/spider/django_scrapy')
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_scrapy.settings")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_scrapy.settings'
    django.setup()


def check_db_connection():
    from django.db import connection

    if connection.connection:
        # NOTE: (zacky, 2016.MAR.21st) IF CONNECTION IS CLOSED BY BACKEND, CLOSE IT AT DJANGO, WHICH WILL BE SETUP AFTERWARDS.
        if not connection.is_usable():
            connection.close()
