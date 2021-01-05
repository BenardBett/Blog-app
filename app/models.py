from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

# from werkzeug.security import generate_password_hash,check_password_hash
# from flask_login import UserMixin
# from . import login_manager
# from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)
    comments=db.relationship('Comment',backref='author',lazy=True)
    pass_secure = db.Column(db.String(255))
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
            return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    __tablename__ = 'posts'
    
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    
    
    
    
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls, id):
        opinions = Post.query.filter_by(id=id).all()
        return opinions

    @classmethod
    def get_all_posts(cls):
        posts = Post.query.order_by('-id').all()
        return posts
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, opinion_id):
        comments = Comment.query.filter_by(opinion_id=opinion_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f"User('{self.date_posted}')"
    
class Quote:
    def __init__ (self,author,quote):
        self.author = author
        self.quote = quote