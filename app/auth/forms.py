from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from app.models import User


class SignUp(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(4)])
    password_check = PasswordField('Password again',
                                   validators=[DataRequired(),
                                               EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        if User.query.all():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists. Try again.')

    def validate_email(self, email):
        if User.query.all():
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists. Try again.')


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4)], default='')
    password = PasswordField('Password', validators=[DataRequired(), Length(4)])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Login')


class RequestResetPassword(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Send link')

    def validate_email(self, email):
        if User.query.all():
            user = User.query.filter_by(email=email.data).first()
            if not user:
                raise ValidationError('There is no account with this email. Try again.')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(4)])
    password_check = PasswordField('Password again',
                                   validators=[DataRequired(),
                                               EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset password')
