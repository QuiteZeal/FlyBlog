# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 22:23
"""
import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from datetime import datetime
import click

from NewLog.blueprints.admin import admin_bp
from NewLog.blueprints.auth import auth_bp
from NewLog.blueprints.blog import blog_bp
from NewLog.config import config
# Use extensions.py to manage flask packages.
from NewLog.extensions import bootstrap, db, pagedown, mail, moment, login_manager, csrf, migrate, toolbar
# context for base.html
from NewLog.models import Admin, Post, Comment, Category, Link
from NewLog.htmltruncate import truncate
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# factory function：create_app()
def create_app(config_name=None):
    if config_name is None:
        # Do Not：app.config.from_pyfile('config.py')
        # Use FLASK_CONFIG in .env to choose.
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('NewLog')
    app.config.from_object(config[config_name])

    app.add_template_filter(truncate)

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commands(app)
    register_logging(app)
    register_request_handlers(app)
    return app


# deploy
def register_logging(app):
    # Mail send error log
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/NewLog.log'),
                                       maxBytes=1024 * 1024 * 15, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=app.config['BLOG_EMAIL'],
        subject='Spring Fly occur Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


# Important!
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)


def register_shell_context(app):
    # For Python Shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


# For html template context
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
    def unauthorized(e):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    # command: flask initial --drop
    # cannot use: init_db, include _ is wrong
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
                body='A self-educated writer'
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


# SQL queries record
def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['BLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\n Query: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response
