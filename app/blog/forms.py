from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    author_name = StringField('昵称', validators=[DataRequired()])
    content = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('提交评论')