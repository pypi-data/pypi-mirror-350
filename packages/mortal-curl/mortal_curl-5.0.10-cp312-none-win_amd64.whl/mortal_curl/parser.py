#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2025/5/26 15:46
@SoftWare: PyCharm
@Project: mortal
@File: parser.py
"""
import ply.yacc as yacc
from .lexer import tokens

_ = tokens


# 语法规则
def p_curl_command(p):
    """curl_command : CURL options"""
    p[0] = {'command': 'curl', 'options': p[2]}


def p_options(p):
    """options : options option
               | option"""
    if len(p) == 3:
        if isinstance(p[1], dict) and isinstance(p[2], dict):
            # 合并头部信息
            if 'headers' in p[1] and 'headers' in p[2]:
                p[1]['headers'].update(p[2]['headers'])
                p[0] = p[1]
            else:
                p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]
    else:
        p[0] = p[1]


def p_option(p):
    """option : request_option
              | header_option
              | binary_option
              | urlencode_option
              | data_option
              | form_option
              | get_option
              | user_option
              | insecure_option
              | params_option
              | cookie_option
              | compress_option
              | url_option"""
    p[0] = p[1]


def p_request_option(p):
    """request_option : REQUEST_OPT STRING
                      | REQUEST_OPT QUOTED_STRING"""
    p[0] = {'method': p[2].upper()}


def p_header_option(p):
    """header_option : HEADER_OPT HEADER
                     | HEADER_OPT QUOTED_STRING"""
    if ':' in p[2]:
        key, value = p[2].split(':', 1)
        if 'sec-ch-ua' not in key.lower() and 'sec-fetch-' not in key.lower() and 'priority' not in key.lower():
            p[0] = {'headers': {key.strip(): value.strip()}}
    else:
        p[0] = {'headers': {p[2]: ''}}


def p_binary_option(p):
    """binary_option : BINARY_OPT STRING
                     | BINARY_OPT QUOTED_STRING"""
    p[0] = {'data': p[2], 'data_type': 'binary'}


def p_urlencode_option(p):
    """urlencode_option : URLENCODE_OPT STRING
                        | URLENCODE_OPT QUOTED_STRING"""
    p[0] = {'data': p[2], 'data_type': 'urlencode'}


def p_data_option(p):
    """data_option : DATA_OPT STRING
                   | DATA_OPT QUOTED_STRING"""
    p[0] = {'data': p[2], 'data_type': 'data'}


def p_form_option(p):
    """form_option : FORM_OPT FORM_DATA
                   | FORM_OPT STRING
                   | FORM_OPT QUOTED_STRING"""
    if '@' in p[2]:
        field, filename = p[2].split('@', 1)
        p[0] = {'form': {field: f'@{filename}'}}
    else:
        p[0] = {'form': p[2]}


def p_get_option(p):
    """get_option : GET_OPT"""
    p[0] = {'method': 'GET'}


def p_user_option(p):
    """user_option : USER_OPT STRING
                   | USER_OPT USER_CRED
                   | USER_OPT QUOTED_STRING"""
    # print(list(p))
    if ':' in p[2]:
        username, password = p[2].split(':', 1)
        p[0] = {'auth': {'username': username, 'password': password}}
    else:
        p[0] = {'auth': {'username': p[2]}}


def p_insecure_option(p):
    """insecure_option : INSECURE_OPT"""
    p[0] = {'verify': False}


def p_params_option(p):
    """params_option : PARAMS"""
    if '&' in p[1]:
        params = {}
        for item in p[1].split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                params[key] = value
        p[0] = {'params': params}
    else:
        if '=' in p[1]:
            key, value = p[1].split('=', 1)
            p[0] = {'params': {key: value}}


def p_cookie_option(p):
    """cookie_option : COOKIE_OPT COOKIE
                     | COOKIE_OPT STRING
                     | COOKIE_OPT QUOTED_STRING"""
    # print(list(p))
    if '=' in p[2]:
        key, value = p[2].split('=', 1)
        p[0] = {'cookies': {key: value}}
    else:
        p[0] = {'cookies': {'name': p[2]}}


def p_compress_option(p):
    """compress_option : COMPRESS_OPT"""
    p[0] = {'compressed': True}


def p_url_option(p):
    """url_option : URL"""
    p[0] = {'url': p[1]}


def p_error(p):
    if p:
        print(f"语法错误在 '{p.value}' (类型: {p.type}, 行: {p.lineno})")
    else:
        print("语法错误在文件结尾")


# 构建语法分析器
parser = yacc.yacc(debug=False)
