# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 13:45
# file_name : log.py


from flask import (Blueprint, request)

from app.shard import db, BaseModel

log = Blueprint("log", __name__, url_prefix="/log")


class Log(BaseModel):
    """用户对于物品的操作记录（购买，查看，评价等）"""
    eventId = db.Column("event_id", db.String(128), nullable=False, comment="事件名称")
    itemId = db.Column("item_id", db.Integer, nullable=False, comment="物品ID")
    userId = db.Column("user_id", db.Integer, nullable=False, comment="用户ID")


@log.route("/put", methods=["GET"])
def save_content():
    try:
        data = request.get_json()

        print(data)
    except Exception as e:
        return {"status": "failed"}
