# app.py
from flask import Flask
from config import Config
from extensions import db, jwt
from models import User
from routes import auth_bp
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)

    @app.route('/')
    def home():
        return "Welcome to the User Microservice!", 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5002)
