# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 10:27
# file_name : content.py

from flask import (Blueprint, request)

content = Blueprint("content", __name__, url_prefix="/content")


@content.route("/put", methods=["GET"])
def save_content():
    data = request.get_json()
    print(data)
    return {'name': 'BieFeNg'}
