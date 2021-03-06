# -*- coding: utf-8 -*-

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from fakeredis import FakeStrictRedis
from werkzeug.local import LocalProxy
from redis import StrictRedis
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})

@login_manager.request_loader
def load_user_from_request(request):

    from red_packet.models.user import User

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

def get_redis():

    from flask import current_app as app

    if app.testing:
        return FakeStrictRedis()
    else:
        redis_url = os.getenv("REDIS_URL", None) or 'redis://localhost:6379'
        return StrictRedis.from_url(redis_url)

redis_store = LocalProxy(get_redis)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
