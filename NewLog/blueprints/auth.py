# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/9 21:07
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'The Login Page'


@auth_bp.route('/logout')
def logout():
    return 'Logout'
