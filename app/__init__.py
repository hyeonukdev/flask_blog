from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db=db)

    with app.app_context():
    # Import parts of our application
        from .api import api as api_blueprint
        from .main import main as main_blueprint
        from .users import users as users_blueprint

        # Register Blueprints
        app.register_blueprint(api_blueprint)
        app.register_blueprint(main_blueprint)
        app.register_blueprint(users_blueprint)



    return app