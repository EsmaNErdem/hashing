from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class UserForm(FlaskForm):
    """Form model for registering new users"""

    username = StringField(
        "Username", 
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=5, max=50)],        
    )
    email = StringField(
        "Email", 
        validators=[InputRequired(), Length(max=50)],
    )
    first_name = StringField(
        'First Name', 
        validators=[InputRequired(), Length(max=30)]
    )
    last_name = StringField(
        'Last Name', 
        validators=[InputRequired(), Length(max=30)]
    )

class LoginForm(FlaskForm):
    """Form Model for login form"""

    username = StringField(
        "Username", 
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=5, max=50)],        
    )

class Delete(FlaskForm):
    """Delete Model Form"""


class FeedbackForm(FlaskForm):
    """FeedBack Model Form"""

    title = StringField(
        "Title", 
        validators=[InputRequired(), Length(min=1, max=100)],
    )
    content = TextAreaField(
        "Content", 
        validators=[InputRequired()],
    )