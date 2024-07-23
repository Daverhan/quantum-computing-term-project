from flask import Flask
from flask_cors import CORS
from app.routes.algorithms import algorithms_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(algorithms_bp, url_prefix='/api/algorithms')

    return app
