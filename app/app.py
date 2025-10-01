from celery import Celery, Task, shared_task
from celery.result import AsyncResult
from flask import Flask, request
import requests
from bs4 import BeautifulSoup 

def celery_init_app(app:Flask) -> Celery:
    Class FlaskTask(Task):
        def __call__(self, *args: Object, *kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app() -> Flask:
    app = Flask("flask-queue")
    app.config.from_mapping(
        CELERY=dict(
            broker_url="amqp://localhost:5672",
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]