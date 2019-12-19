# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 13:45
# file_name : log.py


from flask import (Blueprint, request)

from app.shard import db, BaseModel

log = Blueprint("log", __name__, url_prefix="/log")


class Log(BaseModel):
    eventId = db.Column("event_id", db.String(128), nullable=False, comment="事件名称")


@log.route("/put", methods=["GET"])
def save_content():
    try:
        data = request.get_json()

        print(data)
    except Exception as e:
        return {"status": "failed"}
