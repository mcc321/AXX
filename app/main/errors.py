# -*- coding: utf-8 -*-
from . import main
from flask import jsonify


@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"StatusCode": 400, "info": "客户端请求错误"})


@main.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({"StatusCode": 400, "info": "服务端错误"})
