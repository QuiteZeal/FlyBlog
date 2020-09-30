# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/11 10:44
"""
from NewLog.extensions import db
from NewLog.utils import on_changed_body
# For timestamp
from datetime import datetime
# Generate Password
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin == user log status (is_authenticated, is_active, is_anonymous)
from flask_login import UserMixin

"""
    Flask-SQLAlchemy 模型名稱 --> 表名稱
    如：Admin -->admin, NavBar --> nav_bar
"""


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))  # login_name
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(50))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))  # display_name
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)  # True or False


db.event.listen(Admin.body, 'set', on_changed_body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # posts
    posts = db.relationship('Post', back_populates='category')

    # put the delete post into default category
    def delete(self):
        default_category = Category.query.get(1)  # default category id is 1
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


# class Tag(db.Model):
#     pass  # Create tags


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    slug = db.Column(db.String(200))
    body = db.Column(db.Text(100000))
    body_html = db.Column(db.Text(100000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    private = db.Column(db.Boolean, default=False)

    # Post and Category
    category_name = db.Column(db.String(30), db.ForeignKey('category.name'))
    category = db.relationship('Category', back_populates='posts')

    can_comment = db.Column(db.Boolean, default=True)
    # delete-orphan
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


db.event.listen(Post.body, 'set', on_changed_body)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(255))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # use comment as reply
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    # record comment.id
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
