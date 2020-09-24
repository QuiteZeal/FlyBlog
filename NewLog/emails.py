# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/15 12:52
"""
from flask import url_for, current_app
from flask_mail import Message

from NewLog.extensions import mail

from threading import Thread


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    # use _get_current_object() to get real current app
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#postComment'
    send_mail(subject='New comment', to=current_app.config['BLOG_EMAIL'],
              html='<p>You have New Comment in the article <i>%s</i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">You will encounter a robot when you are going to reply, '
                   'So do not it.:)</small></p>'
                   % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#postComment'
    send_mail(subject='New reply', to=comment.email,
              html='<p>The comment you left in the article <i>%s</i> has a new reply.</p>'
                   '<p><a href="%s">%s</p>'
                   '<p><small style="color: #868e96">You will encounter a robot when you are going to reply, '
                   'So do not it.:)</small></p>'
                   % (comment.post.title, post_url, post_url))
