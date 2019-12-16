from flask import Flask
from flask_migrate import Migrate

from app.config import MYSQL as DATABASE

from app.data_coll.content import content
from app.data_coll.event import event
from app.shard import db
from app.data_coll.user import user

bps = [
    content, event, user
]


def create_app():
    app = Flask(__name__)

    for bp in bps:
        app.register_blueprint(bp)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DATABASE['SQLALCHEMY_TRACK_MODIFICATIONS']
    db.init_app(app)

    Migrate(app, db)
    return app
