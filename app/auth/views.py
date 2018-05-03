from flask import flash, redirect, render_template, url_for

from flask_login import login_required, login_user, logout_user

from . import auth 
from . forms import RegistrationForm, LoginForm

from app import db 
from .. models import Employee

@auth.route('/register', methods=["POST", "GET"])
def register():
    """
    Handles user registration at route /register
    """
    registeration_form = RegistrationForm()
    if registeration_form.validate_on_submit():
        employee = Employee(email=registeration_form.email.data,
                            username=registeration_form.username.data,
                            first_name=registeration_form.first_name.data,
                            last_name=registeration_form.last_name.data,
                            password=registeration_form.password.data)
        db.session.add(employee)
        db.session.commit()
        flash("You have successfully register. You may now login")
        redirect(url_for('auth.login'))
    return render_template('auth/register.html',registeration_form=registeration_form, title="Registration")


@auth.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    """
    Handles user login at /login route
    """
    if login_form.validate_on_submit():
        employee = Employee.query.filter_by(email=login_form.email.data).first()
        if employee is not None and employee.verify_password(login_form.password.data):
            login_user(employee)
            
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            
            else:
                return redirect(url_for("home.dashboard"))
        
        else:
            flash("Invalid Credentials. Please provide valid credential to login.")
    
    return render_template("auth/login.html", login_form=login_form, title="Login")
    
@auth.route("/logout")
@login_required
def logout():
    """
    Handles request for users logout at /logout route
    """
    logout_user()
    flash("You have been successfully logout")
    return redirect(url_for("auth.login"))
 