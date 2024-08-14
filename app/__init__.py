import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    print("Creating Flask application...")
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    print("SQLAlchemy initialized.")

    # Imprimir la ruta de la base de datos
    db_path = os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    print("Database path:", db_path)

    with app.app_context():
        print("Creating all tables...")
        db.create_all()  # Crea todas las tablas definidas en los modelos
        print("Database tables created.")

    from .routes import main_bp
    app.register_blueprint(main_bp)

    from .errors import handle_exception
    app.register_error_handler(Exception, handle_exception)

    return app