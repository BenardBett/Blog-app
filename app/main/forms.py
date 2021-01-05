from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Required



class UpdateAccountForm(FlaskForm):

    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Comment")