# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/16 11:52
# file_name : association_rule.py

from collections import defaultdict
from datetime import datetime
from itertools import combinations

from app.shard import db, BaseModel


class AssociationRule(BaseModel):
    source = db.Column(db.Integer, comment="关联源商品")
    target = db.Column(db.Integer, comment="关联目标商品")
    support = db.Column(db.Float, comment="关联组合出现的次数与所有订单数量的比")
    confidence = db.Column(db.Float, comment="关联组合商品出现次数与关联源商品单独出现次数的比")

    def generate_transaction(self):
        sql_str = "select sku_id,order_no from catering_task order by order_no,sku_id"
        tasks = db.session.execute(sql_str).fetchall()
        transactions = dict()
        for task in tasks:
            order_no = task['order_no']
            sku_id = task['sku_id']
            if order_no not in transactions:
                transactions[order_no] = []
            transactions[order_no].append(sku_id)
        return transactions

    def calculate_itemsets_one(self, transactions, min_sup=0.01):
        N = len(transactions)

        temp = defaultdict(int)
        one_itemsets = dict()

        for key, items in transactions.items():
            for item in items:
                inx = frozenset({item})
                temp[inx] += 1
        for key, itemset in temp.items():
            if itemset > N * min_sup:
                one_itemsets[key] = itemset
        return one_itemsets

    def has_support(self, perm, one_itemsets):
        return frozenset({perm[0]}) in one_itemsets and \
               frozenset({perm[1]}) in one_itemsets

    def calculate_itemsets_two(self, transactions, one_itemsets, min_sup=0.01):
        two_itemsets = defaultdict(int)

        for key, items in transactions.items():
            items = list(set(items))
            if len(items) > 2:
                for perm in combinations(items, 2):
                    if self.has_support(perm, one_itemsets):
                        two_itemsets[frozenset(perm)] += 1
            elif len(items) == 2:
                if self.has_support(items, one_itemsets):
                    two_itemsets[frozenset(items)] += 1
        return two_itemsets

    def calculate_association_rules(self, one_itemsets, two_itemsets, N):
        timestamp = datetime.now()
        rules = []
        for source, source_freq in one_itemsets.items():
            for key, group_freq in two_itemsets.items():
                if source.issubset(key):
                    target = key.difference(source)
                    support = group_freq / N
                    confidence = group_freq / source_freq
                    rules.append((timestamp, next(iter(source)), next(iter(target)),
                                  confidence, support))
                    rule = AssociationRule()
                    rule.target = next(iter(target))
                    rule.source = next(iter(source))
                    rule.confidence = confidence
                    rule.support = support
                    db.session.add(rule)
                    db.session.commit()
        return rules

    def calculate_support_confidence(self, transactions, min_sup=0.01):
        N = len(transactions)

        one_itemsets = self.calculate_itemsets_one(transactions, min_sup)
        two_itemsets = self.calculate_itemsets_two(transactions, one_itemsets, min_sup)
        rules = self.calculate_association_rules(one_itemsets, two_itemsets, N)

        return rules
