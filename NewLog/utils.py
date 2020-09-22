# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/12 16:42
"""
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for

# markdown
from bleach import clean, linkify
from markdown import markdown


# 驗證URL安全性
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# 重定向回上一頁
def redirect_back(default='blog.index', **kwargs):
    # request.args.get('next')和request.referrer是兩種獲取上一頁URL的方式
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


# markdown to html
# def to_html(raw):
#     allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'br', 'strong', 'em', 'b',
#                     'del', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'img',
#                     'a', 'abbr', 'span', 'div', 'table', 'thead', 'tbody', 'tr', 'th', 'td']
#     allowed_attributes = ['src', 'title', 'alt', 'href', 'class']
#     html = markdown(raw, output_format='html', extensions=['tables', 'fenced_code', 'markdown.extensions.codehilite'])
#     clean_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)
#     return linkify(clean_html)


def on_changed_body(target, value, oldvalue, initiator):
    allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'br', 'strong', 'em', 'b',
                    'del', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'img',
                    'a', 'abbr', 'span', 'div', 'table', 'thead', 'tbody', 'tr', 'th', 'td']
    allowed_attributes = ['src', 'title', 'alt', 'href', 'class']
    html = markdown(value, output_format='html', extensions=['tables', 'fenced_code', 'codehilite', 'nl2br'])
    clean_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)
    target.body_html = clean_html

