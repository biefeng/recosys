# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/13 11:45
# file_name : database_migrate.py


from flask_migrate import Migrate
from flask import current_app as app
from app.shard import db

migrate = Migrate(app, db)
