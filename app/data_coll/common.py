# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/19 17:36
# file_name : common.py


import logging

from flask import (Blueprint)

from app.builder.association_rule import AssociationRule

logger = logging.getLogger(__name__)

common = Blueprint("common", __name__, url_prefix="/common")


@common.route("/association_rule", methods=['GET'])
def association_rule():
    """生成关联规则，清除数据库之前的关联规则，并返回关联规则。"""
    assoc_rule = AssociationRule()
    transactions = assoc_rule.generate_transaction()
    rules = assoc_rule.calculate_support_confidence(transactions, 0.01)
    return {"status": "success", "rules": rules}
