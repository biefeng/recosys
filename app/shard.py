# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 11:19
# file_name : shard.py

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class BaseModel(db.Model):
    __abstract__ = True  # 定义为基类

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createDate = db.Column("create_date", db.DateTime, default=datetime.now)

    def __init__(self):
        tablename = self.__tablename__ if self.__tablename__ else self.__class__.__name__.lower()
        table = db.Model.metadata.tables[tablename]
        for key, value in table.columns.items():
            if value.default:
                setattr(self, key, value.default.arg)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
