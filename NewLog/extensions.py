# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/10 16:31
"""
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from Pagedown import PageDown
from flask_debugtoolbar import DebugToolbarExtension

# in __init__.py to init and add parameter
bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
toolbar = DebugToolbarExtension()


@login_manager.user_loader
def load_user(user_id):
    from NewLog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = 'You want to write? Login.'
login_manager.login_message_category = 'warning'
