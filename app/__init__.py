from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.cli import retry_ai_command
    app.cli.add_command(retry_ai_command)  # type: ignore

    return app