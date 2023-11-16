from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email',validators=[ InputRequired(),Email(),Length(min=3, max=50)])
    first_name = StringField('First Name', validators=[InputRequired(),Length(min=1, max=30)])
    last_name=StringField('Last Name', validators=[InputRequired(),Length(min=5, max=30)])
    
class LogInForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class FeedbackForm(FlaskForm):
    title = StringField('Title',validators=[InputRequired(), Length(max=50)])
    content = StringField('Content',validators=[InputRequired(), Length(min=3, max=100)])
    
    
class DeleteForm(FlaskForm):
    """leave black"""
