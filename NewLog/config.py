# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 23:41
"""
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
# For Test: SQLite Memory
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    # use uuid4
    SECRET_KEY = os.getenv('SECRET_KEY', 'spring fly')

    DEBUG_TB_INTERCEPT_REDIRECTS = False  # debug-tool

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # will change at different environment
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')  

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Spring Fly', MAIL_USERNAME)

    # Blog Basic Info
    BLOG_EMAIL = os.getenv('BLOG_EMAIL')
    BLOG_POST_PER_PAGE = 8
    BLOG_MANAGE_POST_PER_PAGE = 18
    BLOG_COMMENT_PER_PAGE = 12
    BLOG_MANAGE_COMMENT_PER_PAGE = 20
    # ('theme name', 'display name')
    BLOG_THEMES = {'sketchy': 'sketchy', 'minty': 'minty', 'flatly': 'flatly'}
    # Slow query 1s
    BLOG_SLOW_QUERY_THRESHOLD = 1


# Inherit BaseConfig
# use config to choose
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


# will use app.config.from_object() in __init__.py
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
