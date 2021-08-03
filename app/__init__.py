from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


db = SQLAlchemy()
migrate = Migrate()

# Login
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'info'


def create_app(config_name):
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db=db)
    login.init_app(app)


    with app.app_context():

        # Import parts of our application
        from .api import api as api_blueprint
        from .main import main as main_blueprint
        from .users import users as users_blueprint

        # Register Blueprints
        app.register_blueprint(api_blueprint)
        app.register_blueprint(main_blueprint)
        app.register_blueprint(users_blueprint)

        # DB create
        db.create_all()


    return app


from app.users import models, views