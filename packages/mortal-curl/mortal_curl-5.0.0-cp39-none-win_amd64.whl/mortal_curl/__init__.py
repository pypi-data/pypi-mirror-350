#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/17 10:11
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["parse_curl"]

from .main import parse_curl

"""
parse_curl: 解析curl命令字符串或文件为结构化字典

参数:
   curl_str (str, optional): 包含curl命令的字符串。与curl_file参数二选一。
   curl_file (str, optional): 包含curl命令的文件路径。与curl_str参数二选一。
   debug (bool, optional): 是否开启调试模式，开启时会打印词法分析结果。默认为False。

返回:
   _Curl: 包含解析结果的_Curl对象
   _Curl 可用属性: 解析curl存在的元素均可直接调用，不存在返回None，如：xxx.url、xxx.headers、xxx.json等
   _Curl 可调用方法: 
      xxx.request_curl(): 返回curl字典，可直接用于requests请求【requests.request(**xxx.request_curl())】
      xxx.pretty(indent=4): 返回美化后的字符串，indent为缩进，默认为4

异常:
   ValueError: 当curl_str和curl_file都未提供时抛出
   lex.LexError: 词法分析错误时抛出
   yacc.YaccError: 语法分析错误时抛出
   Exception: 其他解析错误时抛出
"""
