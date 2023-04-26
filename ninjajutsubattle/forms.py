from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, SelectMultipleField, HiddenField
from wtforms import widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from ninjajutsubattle.models import User, Jutsu
from ninjajutsubattle.controllers import get_element_choices, get_jutsu_choices, get_kekkei_genkai_choices
from flask_login import current_user

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    password_confirmation = PasswordField('Password Confirmation', validators=[DataRequired(), EqualTo('password')])
    register_submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField('Remember me')
    login_submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_pic = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    edit_profile_submit = SubmitField('Confirm Edit')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered in another user')


class PostForm(FlaskForm):
    title = StringField('Subject', validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField('Write your post', validators=[DataRequired()])
    submit_button = SubmitField('Create Post')

class NinjaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    speed = IntegerField('Speed', validators=[DataRequired(), NumberRange(min=1, max=10)])
    body = IntegerField('Body', validators=[DataRequired(), NumberRange(min=1, max=10)])
    mind = IntegerField('Mind', validators=[DataRequired(), NumberRange(min=1, max=10)])
    chakra = IntegerField('Chakra', validators=[DataRequired(), NumberRange(min=1, max=10)])
    element_primary = SelectField('Primary Element', choices=get_element_choices(), validators=[DataRequired()])
    element_secondary = SelectField('Secondary Element', choices=get_element_choices(), validators=[DataRequired()])
    kekkei_genkai = SelectField('Kekkei Genkai', choices=get_kekkei_genkai_choices(), coerce=int)
    basic_jutsus = HiddenField()
    c_rank_jutsus = MultiCheckboxField('Basic Jutsu (Rank C)', choices=get_jutsu_choices('C'), coerce=int)
    b_rank_jutsus = MultiCheckboxField('Basic Jutsu (Rank B)', choices=get_jutsu_choices('B'), coerce=int)
    a_rank_jutsus = MultiCheckboxField('Basic Jutsu (Rank A)', choices=get_jutsu_choices('A'), coerce=int)
    s_rank_jutsus = MultiCheckboxField('Basic Jutsu (Rank S)', choices=get_jutsu_choices('S'), coerce=int)
    submit = SubmitField('Create Ninja')

class NinjaSheetForm(FlaskForm):
    speed = IntegerField('Speed', validators=[NumberRange(min=1, max=20), Optional()])
    body = IntegerField('Body', validators=[NumberRange(min=1, max=20), Optional()])
    mind = IntegerField('Mind', validators=[NumberRange(min=1, max=20), Optional()])
    chakra = IntegerField('Chakra', validators=[NumberRange(min=1, max=20), Optional()])
    experience = IntegerField('XP', validators=[NumberRange(min=0, max=1000), Optional()])
    equipment = TextAreaField('Equipment', validators=[Optional()])
    details = TextAreaField('Details', validators=[Optional()])
    submit_ninja = SubmitField('Save Changes')


