# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 21:07
"""
from flask import Blueprint, render_template, redirect, url_for

from NewLog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from NewLog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
def manage_post():
    return render_template('admin/manage_post.html')


@admin_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm
    return render_template('admin/edit_post.html', form=form)


# 文章刪除後返回上一頁
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
def set_comment(post_id):
    return redirect_back()


@admin_bp.route('/comment/manage')
def manage_comment():
    return render_template('admin/manage_comment.html')


# 評論審核通過
@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
def approve_comment(comment_id):
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    return redirect_back()


@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/new', methods=['GET', 'POST'])
def mew_category():
    form = CategoryForm()
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    form = CategoryForm()
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    return redirect(url_for('.manage_category'))


@admin_bp.route('/link/manage')
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
def new_link():
    form = LinkForm()
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
def edit_link(link_id):
    form = LinkForm()
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
def delete_link(link_id):
    return redirect(url_for('.manage_link'))