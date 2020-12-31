from app import app, rquests,db, bcrypt
from flask import render_template,url_for,flash,redirect,request,abort
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from app.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route("/home")
def home():
    quote = requests.get_quote()
    posts = Post.query.all()
    return render_template('home.html',posts=posts,quote=quote)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home')
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_pasword_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'primary')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',form=form)
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')
            form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Error. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))              
                        