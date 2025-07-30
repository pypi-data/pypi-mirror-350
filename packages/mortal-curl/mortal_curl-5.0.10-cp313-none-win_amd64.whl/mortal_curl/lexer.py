#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2025/5/26 15:46
@SoftWare: PyCharm
@Project: mortal
@File: lexer.py
"""
import ply.lex as lex

# 词法分析器 tokens
tokens = (
    'CURL',
    'REQUEST_OPT',  # -X/--request
    'HEADER_OPT',  # -H/--header
    'DATA_OPT',  # -d/--data/--data-ascii/--data-raw
    'BINARY_OPT',  # --data-binary
    'URLENCODE_OPT',  # --data-urlencode
    'FORM_OPT',  # -F/--form
    'GET_OPT',  # -G/--get
    'USER_OPT',  # -u/--user
    'INSECURE_OPT',  # -k/--insecure
    'COOKIE_OPT',  # -b/--cookie
    'COMPRESS_OPT',  # --compressed
    'URL',
    'PARAMS',
    'HEADER',
    'FORM_DATA',
    'USER_CRED',
    'COOKIE',
    'STRING',
    'QUOTED_STRING',
)


# 词法规则
def t_CURL(t):
    r"""curl\b"""
    return t


def t_REQUEST_OPT(t):
    r"""-(X)|--(request)\b"""
    return t


def t_HEADER_OPT(t):
    r"""-(H)|--(header)\b"""
    return t


def t_BINARY_OPT(t):
    r"""--(data-binary)\b"""
    return t


def t_URLENCODE_OPT(t):
    r"""--(data-urlencode)\b"""
    return t


def t_DATA_OPT(t):
    r"""-(d)|--(data(-ascii)?(-raw)?)\b"""
    return t


def t_FORM_OPT(t):
    r"""-(F)|--(form)\b"""
    return t


def t_GET_OPT(t):
    r"""-(G)|--(get)\b"""
    return t


def t_USER_OPT(t):
    r"""-(u)|--(user)\b"""
    return t


def t_INSECURE_OPT(t):
    r"""-(k)|--(insecure)\b"""
    return t


def t_COOKIE_OPT(t):
    r"""-(b)|--(cookie)\b"""
    return t


def t_COMPRESS_OPT(t):
    r"""--(compressed)\b"""
    return t


def t_URL(t):
    r"""\"(https?|ftp)://[^\?\s]+|\'(https?|ftp)://[^\?\s]+"""
    t.value = t.value[1:-1] if t.value.endswith('"') or t.value.endswith("'") else t.value[1:]
    return t


def t_PARAMS(t):
    r"""\?[^\s]+"""
    t.value = t.value[1:-1] if t.value.endswith('"') or t.value.endswith("'") else t.value[1:]
    return t


def t_HEADER(t):
    r"""[a-zA-Z\-]+:\s*[^\r\n]+"""
    t.value = t.value.strip()
    return t


def t_FORM_DATA(t):
    r"""[^@\s]+@[^\s]+"""
    return t


def t_USER_CRED(t):
    r"""\([^:\s]+:[^:\s]+\)"""
    t.value = t.value[1:-1]
    return t


def t_COOKIE(t):
    r"""[^=\s]+=[^=\s]+"""
    return t


def t_QUOTED_STRING(t):
    r"""\"([^\\\"]|\\.)*\"|\'([^\\\']|\\.)*\'"""
    t.value = t.value[1:-1]
    return t


def t_STRING(t):
    r"""[^\s\'\"]+"""
    if t.value not in ("\\", "\\\\", '$'):
        return t


t_ignore = ' \t\r\n'


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"非法字符 '{t.value[0]}'")
    t.lexer.skip(1)


# 构建词法分析器
lexer = lex.lex()
