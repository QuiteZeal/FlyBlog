# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 21:07
"""
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from datetime import datetime

from NewLog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from NewLog.utils import redirect_back, slugify
from NewLog.extensions import db
from NewLog.models import Post, Category, Comment, Link

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def login_protect():
    pass


@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.body = form.body.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title = current_user.blog_sub_title
    form.body.data = current_user.body
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        if form.slug.data:
            slug = form.slug.data
        else:
            slug = slugify(form.title.data)
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, slug=slug, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post published.', 'success')
        return redirect(url_for('blog.show_post', slug=post.slug))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        if form.slug.data:
            post.slug = form.slug.data
        else:
            post.slug = slugify(form.title.data)
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        post.last_timestamp = datetime.utcnow()
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', slug=post.slug))
    form.title.data = post.title
    form.slug.data = post.slug
    form.body.data = post.body
    form.category.data = post.category_name
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post already gone.', 'success')
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/hide', methods=['POST'])
def hide_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.private:
        post.private = False
        flash('Post is shown.', 'success')
    else:
        post.private = True
        flash('Post is hidden.', 'success')
    db.session.commit()
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disabled.', 'success')
    else:
        post.can_comment = True
        flash('Comment enabled.', 'success')
    db.session.commit()
    return redirect_back()


@admin_bp.route('/comment/manage')
def manage_comment():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'unreviewed', 'admin'
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_MANAGE_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query
    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category: {} created.'.format(name), 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<category_name>/edit', methods=['GET', 'POST'])
def edit_category(category_name):
    form = CategoryForm()
    category = Category.query.filter_by(name=category_name).first_or_404()
    if category.id == 1:
        flash('Unnamed is well, Do not change it.', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category: {} updated.'.format(category_name), 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<category_name>/delete', methods=['POST'])
def delete_category(category_name):
    category = Category.query.filter_by(name=category_name).first_or_404()
    if category.id == 1:
        flash('You can not do this! Unless you want to drop the whole site.', 'danger')
        return redirect(url_for('blog.index'))
    category.delete()  # use Category.delete() in models.py
    flash('Category: {} deleted.'.format(category_name), 'success')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/link/manage')
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash('Link: {} created.'.format(name), 'success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash('Link: {} updated.'.format(link.name), 'success')
        return redirect(url_for('.manage_link'))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link: {} deleted.'.format(link.name), 'success')
    return redirect(url_for('.manage_link'))
