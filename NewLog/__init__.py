# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 22:23
"""
import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from datetime import datetime
import click

from NewLog.blueprints.admin import admin_bp
from NewLog.blueprints.auth import auth_bp
from NewLog.blueprints.blog import blog_bp
from NewLog.config import config
# flask擴展包，單獨放在extensions.py中
from NewLog.extensions import bootstrap, db, pagedown, mail, moment, login_manager, csrf
# 創建base.html上下文
from NewLog.models import Admin, Post, Comment, Category, Link


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


# 注册后才能使用！！
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)


def register_shell_context(app):
    # 配置Python Shell上下文
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


# 處理模板上下文，重要！
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        date_now = datetime.utcnow()
        # unread_comments
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories, links=links,
            date_now=date_now, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('400.html', description=e.description), 400

    @app.errorhandler(401)
    def bad_request(e):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def bad_request(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    # command: flask initial --drop
    # cannot use: init_db, than is wrong
    # 可手動刪除數據表後重建
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initial(drop):
        """
            Initialize the database
            usage: $ flask initial --drop
        """
        if drop:
            click.confirm('Seriously? This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop all tables done!')
        db.create_all()
        click.echo('Reinitialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10. Use --category=[num] to set.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50. Use --post=[num] to set.')
    @click.option('--comment', default=200, help='Quantity of comments, default is 200. Use --comment=[num] to set.')
    def forge(category, post, comment):
        from NewLog.fakes import fake_admin, fake_categories, fake_comments, fake_links, fake_posts
        """
            Generate fake data
            usage: flask forge --category/post/comment=[num]
        """
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')

    # Initialize Administrator
    @app.cli.command()
    @click.option('--username', prompt=True, help='Set admin login username.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='Set admin login password.')
    def initialize(username, password):
        """
        Initialize Administrator Account
        """
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating account...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating new administrator account...')
            admin = Admin(
                username=username,
                blog_title='Spring Fly',
                blog_sub_title='Thinking and write.',
                name='Spring Fly',
                about='A self-educated writer'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Initialize the category...')
            category = Category(name='Unnamed')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')
