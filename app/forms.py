from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import sqlalchemy as sa

from app import db
from app.models import User
import app.helpers as helpers


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 6)])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validation_username(self, username: str) -> None:
        registered_user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if registered_user is not None:
            raise ValidationError("User with that username already exists.")

    def validation_email(self, email: str) -> None:
        registered_email = db.session.scalar(sa.select(User).where(User.email == email.data))
        if registered_email is not None:
            raise ValidationError("Email already exists.")


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about = TextAreaField('About me', validators=[Length(min=0, max=200)])
    submit = SubmitField('Update')
    
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self, username: str):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
    
    def validate_about(self, about: str):
        print(about.data)
        if about.data != "":
            if helpers.check_profanity(about.data):
                raise ValidationError('Please, don\'t use censor words.')
    
    
class FollowForm(FlaskForm):
    submit = SubmitField('Submit')
