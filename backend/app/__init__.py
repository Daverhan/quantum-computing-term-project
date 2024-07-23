from flask import Flask
from app.routes.algorithms import algorithms_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(algorithms_bp, url_prefix='/api/algorithms')

    return app
