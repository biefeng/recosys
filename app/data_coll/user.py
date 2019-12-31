# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 10:28
# file_name : user.py

import logging

import csv

from io import BufferedReader, StringIO

from flask import (Blueprint, request)
from werkzeug.utils import secure_filename
from app.shard import db, BaseModel

logger = logging.getLogger(__name__)

user = Blueprint("user", __name__, url_prefix="/user")


# Model
class User(BaseModel):
    """用户"""
    userName = db.Column("user_name", db.String(128), comment="用户名")

    def __init__(self, user_name):
        self.userName = user_name


# Router
@user.route("/put", methods=["POST"])
def save_content():
    """
    添加用户
    :return:
    """
    try:
        data = request.get_json()
        curr = User(data["userName"])
        db.session.add(curr)
        db.session.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


@user.route("/upload", methods=["POST"])
def upload():
    result = {"status": "success"}
    if "file" not in request.files:
        result['status'] = "failed"
        result["msg"] = "未提供文件"
    else:
        file = request.files['file']
        if file.filename == '':
            result['status'] = "failed"
            result["msg"] = "未提供文件"
        else:
            filename = secure_filename(file.filename)
            s = str(file.stream.read())
            string_io = StringIO(s)
            reader = csv.DictReader(string_io, delimiter=' ', fieldnames=["sku_id", "sku_name"])
            for row in reader:
                print(row)
            print(filename)
            print(file.content_type)

    return result
