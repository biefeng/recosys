# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/19 17:31
# file_name : item.py


import logging

from flask import (Blueprint, request)

from app.shard import db, BaseModel

logger = logging.getLogger(__name__)

item = Blueprint("item", __name__, url_prefix="/item")


# Model
class Item(BaseModel):
    """内容/物品"""
    itemName = db.Column("item_name", db.String(128), comment="内容名称")
    itemCode = db.column("item_code", db.String(64), comment="内容编码")


# Router
@item.route("/put", methods=["POST"])
def save_content():
    try:
        data = request.get_json()
        add = Item()
        add.itemName = data['skuName']
        add.itemCode = data['skuId']
        db.session.add(add)
        db.session.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
