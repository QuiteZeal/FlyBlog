# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 21:07
"""
from flask import Blueprint, render_template, request, current_app, abort, make_response, flash, redirect, url_for

from NewLog.emails import send_new_comment_email, send_new_reply_email
from NewLog.models import Post, Category, Comment
from NewLog.utils import redirect_back
from NewLog.forms import AdminCommentForm, CommentForm
from NewLog.extensions import db

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('blog/index.html', posts=posts)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    # return 'The About Page'
    return render_template('blog/about.html')


@blog_bp.route('/overview')
def overview():
    return render_template('blog/overview.html')


@blog_bp.route('/category/<category_name>')
def show_category(category_name):
    category = Category.query.filter_by(name=category_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    # Add query filter
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    # desc() = descending, asc() = ascending
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    # if current_app.is_authenticated:
    #     form = AdminCommentForm()
    #     form.author.data = current_user.name  # need Flask-Login

    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Only Read, No Discuss.', 'warning')
        return redirect(
            url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#commentForm'
        )


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=60 * 60 * 24 * 30)
    return response
