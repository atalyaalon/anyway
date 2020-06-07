# -*- coding: utf-8 -*-
import os
from .parsers import secrets

#
# This is the configuration file of the application
#
# Please make sure you don't store here any secret information and use environment
# variables
#

APP_SECRET_KEY = secrets.get('APP_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres@localhost/anyway")
SQLALCHEMY_TRACK_MODIFICATIONS = True
ENTRIES_PER_PAGE = os.environ.get("ENTRIES_PER_PAGE", 1000)
SQLALCHEMY_POOL_RECYCLE = 60

# available languages
LANGUAGES = {"en": "English", "he": "עברית"}
