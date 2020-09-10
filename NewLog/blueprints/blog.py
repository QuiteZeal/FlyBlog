# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 21:07
"""
from flask import Blueprint

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/about')
def about():
    return 'The About Page'


@blog_bp.route('/category/<int:category_id>')
def category(category_id):
    return 'The Category Page'
