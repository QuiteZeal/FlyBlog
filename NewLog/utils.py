# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/12 16:42
"""
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for


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