from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .config import Config

login_manager = LoginManager()
login_manager.login_view = "main.login"
csrf = CSRFProtect()

engine = None
SessionLocal = None

def create_app():
    global engine, SessionLocal
    app = Flask(__name__)
    app.config.from_object(Config)
#Wenn CSRF aktiv, dann funktioniert Hydra nicht
    app.config['WTF_CSRF_ENABLED'] = False

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], pool_pre_ping=True, future=True)
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False))

    login_manager.init_app(app)
    csrf.init_app(app)

    from .models import Base
    Base.metadata.create_all(engine)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
