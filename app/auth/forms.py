from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from .. models import Employee

class RegistrationForm(FlaskForm):
    """
    For for user to register
    """
    email = StringField("Email", validators=[DataRequired("Please enter an email"), Email()])
    username = StringField("Username", validators=[DataRequired("Please enter a user name")])
    first_name = StringField("First Name", validators=[DataRequired("Please enter a first name")])
    last_name = StringField("Last Name", validators=[DataRequired("Please enter a last name")])
    password = PasswordField("Password", validators=[DataRequired("Please enter a password"), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField("Register")
    
    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError("This email has already been registered")
    
    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already in use")

class LoginForm(FlaskForm):
    """
    A form to login the user
    """
    email = StringField("Email", validators=[DataRequired("Please enter an email")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    submit = SubmitField("Login")