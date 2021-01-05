from . import auth
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from ..models import User
from ..request import get_quote
from .forms import  LoginForm,RegistrationForm
from .. import db
from app import bcrypt
from ..email import mail_message

# from flask.ext.bcrypt import Bcrypt
# from ..email import mail_message

@auth.route("/register",methods=['GET','POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home')
    
    quote = get_quote()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to My-blog website","email/welcome_user",user.email,user=user)

        flash('Your account has been created', 'primary')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register',form=form)
    

@auth.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:orm =RegistrationForm()
    #     return redirect(url_for('home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            
            return redirect(url_for('main.home'))
        else:
            flash('Error. Please check your email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)
    
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))   
