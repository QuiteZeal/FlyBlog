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
# 使用SQLite內存型數據庫，測試用
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# 以下為基本配置
class BaseConfig(object):
    # 需要在部署前隨即生成
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Spring Fly', MAIL_USERNAME)

    # 博客頁面的配置變量
    BLOG_EMAIL = os.getenv('BLOG EMAIL')
    BLOG_POST_PER_PAGE = 8
    BLOG_MANAGE_POST_PER_PAGE = 18
    BLOG_COMMENT_PER_PAGE = 12
    # ('theme name', 'display name')
    BLOG_THEMES = {'sketchy': 'sketchy', 'minty': 'minty', 'flatly': 'flatly', 'darkly': 'darkly'}


# 根據BaseConfig擴展
# 開發、測試、發布時選用不同的數據庫配置
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}