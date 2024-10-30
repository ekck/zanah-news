from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
   

    # Error handling
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Initialize admin after other blueprints
    from app.admin import bp as admin_bp, init_admin
    app.register_blueprint(admin_bp, url_prefix='/admin-custom')
    init_admin(app, db)

    # Logging setup
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/newsscraper.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('News Scraper startup')

    return app

# Import models here
from app.models import user