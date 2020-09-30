# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://spring-fly.com
    @Create: 2020/9/11 22:00
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    SelectField, ValidationError, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional
# from flask_ckeditor import CKEditorField
from flask_pagedown.fields import PageDownField

# Custom validator for category
from NewLog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 60)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 120)])
    body = PageDownField('About Me', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 100)])
    category = SelectField('Category', coerce=int, default=1)
    slug = StringField('Slug', validators=[Optional(), Length(0, 60)])
    body = PageDownField('Body', validators=[DataRequired()])
    submit = SubmitField()

    # for <option>
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('{} already exists.'.format(field.data))


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 255)])
    site = StringField('Site', validators=[Optional(), URL(message='need prefix like https://'), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


# Inherit CommentFrom and add hidden info
class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(message='need prefix like https://'), Length(1, 255)])
    submit = SubmitField()
