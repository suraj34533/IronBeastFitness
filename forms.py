from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=20)],
                          render_kw={"class": "w-full bg-gray-900 border border-gray-700 rounded-md py-2 px-3 text-white golden-input focus:border-gold-500", 
                                    "placeholder": "Enter username"})
    
    email = StringField('Email',
                       validators=[DataRequired(), Email()],
                       render_kw={"class": "w-full bg-gray-900 border border-gray-700 rounded-md py-2 px-3 text-white golden-input focus:border-gold-500", 
                                 "placeholder": "Enter email"})
    
    password = PasswordField('Password',
                           validators=[DataRequired(), Length(min=8)],
                           render_kw={"class": "w-full bg-gray-900 border border-gray-700 rounded-md py-2 px-3 text-white golden-input focus:border-gold-500", 
                                     "placeholder": "Enter password"})
    
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
                                   render_kw={"class": "w-full bg-gray-900 border border-gray-700 rounded-md py-2 px-3 text-white golden-input focus:border-gold-500", 
                                             "placeholder": "Confirm password"})
    
    submit = SubmitField('Register',
                       render_kw={"class": "pixel-button w-full"})
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Username or Email',
                          validators=[DataRequired()],
                          render_kw={"class": "w-full bg-gray-900 border border-gray-700 rounded-md py-2 px-3 text-white golden-input focus:border-gold-500", 
                                    "placeholder": "Enter username or email"})
    
    password = PasswordField('Password',
                           validators=[DataRequired()],
                           render_kw={"class": "w-full bg-gray-900 border border-gray-700 rounded-md py-2 px-3 text-white golden-input focus:border-gold-500", 
                                     "placeholder": "Enter password"})
    
    remember = BooleanField('Remember Me',
                           render_kw={"class": "golden-checkbox"})
    
    submit = SubmitField('Login',
                       render_kw={"class": "pixel-button w-full"})