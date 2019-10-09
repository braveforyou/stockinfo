# -*- coding: utf-8 -*-
"""
Created on 2018/1/17 13:13

@Author: Kun
"""
import json
from flask import jsonify


class ResponseVo(object):
    def __init__(self, success, message="", errorCode=0, data=None, *args, **kwargs):
        self.success = success
        self.message = message
        self.errorCode = errorCode

        if data is not None:
            if isinstance(data, dict):
                self.data = data
            elif isinstance(data, str):
                self.data = json.loads(data)
            else:
                self.data = data
        else:
            self.data = data

        super(ResponseVo, self).__init__()

    def to_dict(self):
        return {"success": self.success, "message": self.message, "errorCode": self.errorCode, "data": self.data}

    def to_vo(self):
        resp_vo = jsonify(self.to_dict())
        resp_vo.headers['Access-Control-Allow-Origin'] = '*'
        return resp_vo
