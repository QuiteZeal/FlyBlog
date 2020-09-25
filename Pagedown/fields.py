# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/25 21:11
"""
from wtforms.fields import TextAreaField
from .widgets import PageDown


class PageDownField(TextAreaField):
    widget = PageDown()
