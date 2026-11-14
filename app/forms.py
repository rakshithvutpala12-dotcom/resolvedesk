from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email address', validators=[DataRequired(), Email(), Length(max=160)])
    department = StringField('Department', validators=[Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')

class TicketForm(FlaskForm):
    title = StringField('Issue title', validators=[DataRequired(), Length(max=180)])
    category = SelectField('Category', choices=[('Hardware','Hardware'),('Software','Software'),('Network','Network'),('Account & Access','Account & Access'),('Other','Other')], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')], validators=[DataRequired()])
    description = TextAreaField('Describe the issue', validators=[DataRequired(), Length(min=10, max=5000)])
    submit = SubmitField('Submit ticket')

class CommentForm(FlaskForm):
    body = TextAreaField('Add a comment', validators=[DataRequired(), Length(min=2, max=2000)])
    submit = SubmitField('Post comment')
