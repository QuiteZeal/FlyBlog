# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/11 10:44
"""
# 創建管理員模型:Admin, Category
from NewLog.extensions import db

# 用於生成timestamp
from datetime import datetime

# Generate Password
from werkzeug.security import generate_password_hash, check_password_hash

# UserMixin == user log status
# is_authenticated, is_active, is_anonymous
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
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)  # True or False


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # posts
    posts = db.relationship('Post', back_populates='category')

    # 後台管理：刪除分類
    # 禁止刪除默認分類，將刪除分類後的文章移入默認分類中
    def delete(self):
        default_category = Category.query.get(1)  # 獲取默認分類
        posts = self.posts[:]
        for post in posts:
            post.category = default_category  # 遍歷post，賦值為默認分類
        db.session.delete(self)
        db.session.commit()


# class Tag(db.Model):
#     pass  # Create tags


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    # length = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # 建立Post與Category之間的關係
    category_name = db.Column(db.String(30), db.ForeignKey('category.name'))
    category = db.relationship('Category', back_populates='posts')

    can_comment = db.Column(db.Boolean, default=True)
    # delete-orphan 可以將評論comments從文章post中移除
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(255))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # 添加回復，回復本身也是評論，添加外鍵指向自身
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
