# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 10:28
# file_name : user.py

import logging

from flask import (Blueprint, request)

from app.builder.association_rule import AssociationRule
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
    try:
        data = request.get_json()
        curr = User(data["userName"])
        db.session.add(curr)
        db.session.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


@user.route("/ass", methods=['GET'])
def ass():
    # try:
    association_rule = AssociationRule()
    transactions = association_rule.generate_transaction()
    rules = association_rule.calculate_support_confidence(transactions, 0.01)
    return {"status": "success", "rules": rules}
    # except Exception as E:
    #     print(E)
    #     print("异常")
    #     return {"status": "failed"}
