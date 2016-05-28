# 创建表单

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class LoginForm(Form):
    account = StringField('account', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
    about_me = TextAreaField('about_me', validators=[DataRequired()])


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])


class CollectionForm(Form):
    title = StringField('collection', validators=[DataRequired()])
    description = StringField("description", validators=[])


class StarForm(Form):
    star = RadioField('star', coerce=int)
