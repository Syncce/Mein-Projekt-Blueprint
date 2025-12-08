import os
from dotenv import load_dotenv

# Pfad zur .env relativ zum Projekt-Hauptverzeichnis:
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_ME_bf72c954d3825be8") # Nicht wichtig, da .env datei erstellt.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")