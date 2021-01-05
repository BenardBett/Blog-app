from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateAccountForm,PostForm,CommentForm
from ..models import User,Post,Comment
from   ..request import get_quote
from flask_login import login_required,current_user
from .. import db,photos
import markdown2


@main.route("/")
def home():
    
    quote = get_quote()
    posts = Post.query.all()
    return render_template('home.html',posts=posts,quote=quote)
content = "WELCOME TO MY-BLOG WEBSITE"
quote = get_quote()

@main.route('/user/<uname>')
def profile(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, quote=quote)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, quote=quote)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account is updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data == current_user.username
        form.email.data == current_user.email
    return render_template('account.html', title='Account', form=form)


@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        # flash('Your post has been created!', 'primary')
        return redirect(url_for('main.home'))
    return render_template('blog.html', title='New Post',form=form, legend='New Post')
    
@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = Comment.query.all()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data)
        db.session.add(comment)
        db.session.commit()
        # flash('Your comment has been posted!', 'primary')
        return redirect(url_for('main.home'))
    return render_template('update.html', title=post.title, post=post, form=form, comments=comments)




@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_blog.html', title='Update Blog', form=form, legend='Update Blog')

@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    # flash('Blog deleted!', 'primary')
    return redirect(url_for('home'))


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(post_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'primary')
    return redirect(url_for('main.home'))


