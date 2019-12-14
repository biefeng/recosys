# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 11:20
# file_name : config.py

MYSQL = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:Biefeng123!@192.168.186.135/recosys',
    'SQLALCHEMY_POOL_SIZE': 10,
    'SQLALCHEMY_POOL_RECYCLE': 3600,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'mysql_engine': 'InnoDB'
    }
}

SQLITE = {
    'SQLALCHEMY_DATABASE_URI': '////tmp/test.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}
