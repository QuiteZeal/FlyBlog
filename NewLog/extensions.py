# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/10 16:31
"""
# 導入flask擴展包的內容單獨寫在extensions.py
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment

# 先不傳入參數
bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()