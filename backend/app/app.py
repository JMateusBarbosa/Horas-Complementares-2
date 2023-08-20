from flask import Flask

def create_app():
    app = Flask(__name__)

    # Aqui você pode configurar e inicializar extensões, blueprints, etc.

    return app

