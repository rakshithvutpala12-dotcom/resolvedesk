from flask import Flask
from config import Config
from .extensions import db, login_manager, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    from .cli import create_admin
    app.cli.add_command(create_admin)
    from .auth import bp as auth_bp
    from .main import bp as main_bp
    from .tickets import bp as tickets_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    with app.app_context():
        db.create_all()
    return app
