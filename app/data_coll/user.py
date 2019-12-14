# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 10:28
# file_name : user.py

from flask import (Blueprint, request)

from app.data_coll.shard import db, BaseModel

import logging

logger = logging.getLogger(__name__)

user = Blueprint("user", __name__, url_prefix="/user")


# Model
class User(BaseModel):
    userName = db.Column("user_name", db.String(128), comment="用户名")

    def __init__(self, user_name):
        self.userName = user_name


# Router
@user.route("/put", methods=["POST"])
def save_content():
    try:
        data = request.get_json()
        curr = User(data["userName"])
        db.session.add(curr)
        db.session.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
