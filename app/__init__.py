from flask import Flask

from .views.account import acc_bp
from .views.index import index_bp


def create_app():
    my_app = Flask(__name__)
    my_app.config.from_object('settings.Config')

    my_app.register_blueprint(acc_bp)
    my_app.register_blueprint(index_bp)

    return my_app
