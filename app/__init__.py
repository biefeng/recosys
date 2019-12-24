from flask import Flask
from flask_migrate import Migrate

from app.config import MYSQL as DATABASE
from app.data_coll.content import content
from app.data_coll.event import event
from app.data_coll.user import user
from app.data_coll.log import log

from app.shard import db

bps = [
    content, event, user, log
]


def create_app():
    app = Flask(__name__)

    for bp in bps:
        app.register_blueprint(bp)
    # 配置数据库链接
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DATABASE['SQLALCHEMY_TRACK_MODIFICATIONS']
    # 配置文件上传上限Size：16M
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)

    Migrate(app, db)
    return app
