# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 22:23
"""
import os

from flask import Flask, render_template
import click

from NewLog.blueprints.admin import admin_bp
from NewLog.blueprints.auth import auth_bp
from NewLog.blueprints.blog import blog_bp
from NewLog.config import config
# flask擴展包，單獨放在extensions.py中
from NewLog.extensions import bootstrap, db, ckeditor, mail, moment


# 組織工廠函數：create_app()
def create_app(config_name=None):
    if config_name is None:
        # 不直接用：app.config.from_pyfile('config.py')
        # 而是可以選擇配置：開發、測試、發布
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('NewLog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commands(app)
    return app


# 定義註冊函數
def register_logging(app):
    pass  # 部署上線


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)


def register_shell_context(app):
    # 配置Python Shell上下文
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    # command: flask init_db --drop
    # 可手動刪除數據表後重建
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def init_db(drop):
        """
            Initialize the database
            usage: $ flask init_db --drop
        """
        if drop:
            click.confirm('Seriously? This operation will delete the whole database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop all tables done!')
        db.create_all()
        click.echo('Reinitialized database.')


