#!/usr/bin/env python3
# -*- coding: utf-8 -*-


configs = {
    'debug': True,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'www',
        'password': 'www',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}

# 用于处理需要一次性初始化的控制参数，这些数据几乎不会变
init = False
# 用于控制那些每天会变得数据，在debug模式下使用一份缓存即可
debug = False

period="D"

#period="W"
