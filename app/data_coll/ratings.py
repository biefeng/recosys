# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 13:45
# file_name : log.py


from _collections import defaultdict

from flask import (Blueprint)
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import func, distinct, case

from app.data_coll.log import Log
from app.shard import db, BaseModel

ratings = Blueprint("ratings", __name__, url_prefix="/ratings")

w1 = 100
w2 = 50
w3 = 20


class Ratings(BaseModel):
    """ 用户评分数据 """
    rating = db.Column("rating", db.String(16), nullable=False, comment="评分")
    itemId = db.Column("item_id", db.Integer, nullable=False, comment="物品ID")
    userId = db.Column("user_id", db.Integer, nullable=False, comment="用户ID")
    rating_timestamp = db.Column("rating_timestamp", db.DateTime, comment="时间戳")
    type = db.Column("type", db.String(32), default="implicit", comment="类型：显式/隐式")


def query_log_for_users():
    """
    Equivalent to following sql:

    select distinct(user_id)
    from collector_log log
    """
    return db.session.query(distinct(Log.userId)).all()


def calculate_ratings():
    rows = query_log_for_users()
    print("data loaded,starting to calculate")
    for row in rows:
        userid = row[0]
        ratings = calculate_implicit_ratings_for_user(userid)
        break
        # save_ratings(ratings, userid, 'implicit')
    return rows


def calculate_implicit_ratings_for_user(user_id):
    data = query_aggregated_log_data_for_user(user_id)

    # agg_data = dict()
    # max_rating = 0
    #
    # for row in data:
    #     content_id = str(row['content_id'])
    #     if content_id not in agg_data.keys():
    #         agg_data[content_id] = defaultdict(int)
    #
    #     agg_data[content_id][row['event']] = row['count']
    #
    # ratings = dict()
    # for k, v in agg_data.items():
    #     rating = w1 * v['buy'] + w2 * v['details'] + w3 * v['moredetails']
    #     max_rating = max(max_rating, rating)
    #
    #     ratings[k] = rating
    #
    # for content_id in ratings.keys():
    #     ratings[content_id] = 10 * ratings[content_id] / max_rating
    #
    # return ratings


def query_aggregated_log_data_for_user(userid):
    # pass
    buy_count = case([
        (Log.eventId == 1, 1)
    ])

    user_data = db.session.query(Log.userId, Log.itemId,
                                 func.count(buy_count).label("buy_count")).group_by(Log.userId, Log.itemId).order_by(
        Log.userId).all()
    print(user_data)
    # user_data = Log.query.filter_by(user_id=userid).values('user_id',
    #                                                       'content_id',
    #                                                       'event').annotate(count=Count('created'))
    # return user_data


@ratings.route("/calculate", methods=["GET"])
def calculate():
    try:
        values = calculate_ratings()
        print(values)
        queries = get_debug_queries()
        print(queries[0][0])
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed"}
