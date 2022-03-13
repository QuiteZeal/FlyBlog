# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/12 18:14
"""
import random

from NewLog import db
from NewLog.models import Admin, Category, Comment, Post, Link

# avoid same name
from sqlalchemy.exc import IntegrityError
from faker import Faker

# fake = Faker('zh_CN') # or zh_TW
fake = Faker()


# dont use fake
def fake_admin():
    admin = Admin(
        username='fly',
        blog_title='Spring Fly',
        blog_sub_title='Just for Writing.',
        name='Fly',
        body='From here, to write there.'
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            slug=fake.uuid4(),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=200):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    # set salt
    salt = int(count * 0.2)
    for i in range(salt):
        # random generate unreviewed comments
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # generate admin comments
        comment = Comment(
            author='Fly',
            email='fly@quitezeal.com',
            site='spring-fly.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # generate replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    springfly = Link(name='Spring-Fly', url='#')
    ahaknow = Link(name='AhaKnow', url='https://ahaknow.com')
    quitezeal = Link(name='QuiteZeal', url='https://quitezeal.com')
    db.session.add_all([springfly, ahaknow, quitezeal])
    db.session.commit()
