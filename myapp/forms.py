from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from sqlalchemy import select, or_
from . import SessionLocal
from .models import User

class RegisterForm(FlaskForm):
    username = StringField("Benutzername", validators=[
        DataRequired(message="Bitte einen Benutzernamen eingeben."),
        Length(min=3, max=30, message="Der Benutzername muss zwischen 3 und 30 Zeichen lang sein.")
    ])
    email = StringField("E-Mail", validators=[
        DataRequired(message="Bitte eine gültige E-Mail eingeben."),
        Email(message="Bitte eine gültige E-Mail-Adresse verwenden."),
        Length(max=255)
    ])
    password = PasswordField("Passwort", validators=[
        DataRequired(message="Bitte ein Passwort eingeben."),
        Length(min=6, max=128, message="Das Passwort muss mindestens 6 Zeichen lang sein.")
    ])
    confirm = PasswordField("Passwort bestätigen", validators=[
        DataRequired(message="Bitte das Passwort bestätigen."),
        EqualTo("password", message="Passwörter stimmen nicht überein.")
    ])
    submit = SubmitField("Registrieren")

    def validate_username(self, field):
        """Prüft, ob der Benutzername bereits existiert."""
        with SessionLocal() as db:
            existing_user = db.execute(select(User).where(User.username == field.data)).scalar_one_or_none()
            if existing_user:
                raise ValidationError("Dieser Benutzername ist bereits vergeben.")

    def validate_email(self, field):
        """Prüft, ob die E-Mail bereits existiert."""
        with SessionLocal() as db:
            existing_email = db.execute(select(User).where(User.email == field.data)).scalar_one_or_none()
            if existing_email:
                raise ValidationError("Diese E-Mail wird bereits verwendet.")

class LoginForm(FlaskForm):
    identifier = StringField("Benutzername oder E-Mail", validators=[DataRequired()])
    password = PasswordField("Passwort", validators=[DataRequired()])
    submit = SubmitField("Einloggen")

class PostForm(FlaskForm):
    title = StringField("Titel", validators=[DataRequired(), Length(min=3, max=120)])
    body = TextAreaField("Inhalt (max. 2000 Zeichen)", validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField("Veröffentlichen")
