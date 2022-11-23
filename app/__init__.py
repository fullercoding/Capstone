from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login = LoginManager()
moment = Moment()

def create_app(config_class=Config):
    # intializing
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    login.login_view = 'auth.login'
    login.login_message = 'Log yourself in your flithy animal!'
    login.login_message_category = 'warning'



    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models