from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.orm import converts, model_form, ModelConverter
from wtforms import fields

from application.models import User, UserStatusEnum, Shipment, Widget
from application import db


class Converter(ModelConverter):
    @converts("Enum")
    def conv_Enum(self, column, field_args, **extra):
        field_args["choices"] = [(e, e) for e in column.type.enums]
        return fields.SelectMultipleField(**field_args)

class Customer:
    def validate_customer(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists please register with another')


WidgetForm = model_form(Widget,base_class = FlaskForm ,db_session=db.session, field_args = {
        'name' : {
            'validators' : [DataRequired(),Length(max=50)]
        }
    }, converter=Converter())

        
ShipmentForm = model_form(Shipment,base_class = FlaskForm ,db_session=db.session)


class RegistrationForm(FlaskForm):
    mychoices = [(UserStatusEnum.customer.value), (UserStatusEnum.supplier.value)]
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    user_status = SelectField(u'Are you',choices = mychoices, validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists please register with another')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists please register with another')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')