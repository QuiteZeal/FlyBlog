# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/10 16:31
"""
# 導入flask擴展包的內容單獨寫在extensions.py
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_ckeditor import CKEditor
from flask_pagedown import PageDown
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
# from flask_sslify import SSLify

# 先不傳入參數
bootstrap = Bootstrap()
db = SQLAlchemy()
# ckeditor = CKEditor()
pagedown = PageDown()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
# sslify = SSLify()


@login_manager.user_loader
def load_user(user_id):
    from NewLog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = 'You want to write? Login.'
login_manager.login_message_category = 'warning'
