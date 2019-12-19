# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 10:28
# file_name : event.py


from flask import (Blueprint, request)
from app.shard import db, BaseModel

event = Blueprint("event", __name__, url_prefix="/event")


class Event(BaseModel):
    eventName = db.Column(db.String(128), nullable=False, comment="事件名称")


@event.route("/add", methods=["POST"])
def save_content():
    data = request.get_json()
    if data is not None:
        add = Event()
        add.eventName = data['eventName']
        db.session.add(add)
        db.session.commit()
    return {'name': 'BieFeNg'}
