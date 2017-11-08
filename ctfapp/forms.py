from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, ValidationError
from wtforms import TextAreaField
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask_login import current_user
from .model import User, Spend
from ctfapp import sk_pem
from .util import check_coin, get_coin_MD5
import json


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.Regexp(
            '^[a-zA-Z0-9_]*$', message='Only alphanumeric and _ allowed!')
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Repeat Password')

    def validate_username(form, field):
        user = User.query.filter(User.username == field.data).first()
        if user is not None:
            raise ValidationError("That User already exists!")


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])

    def validate_password(form, field):
        try:
            user = User.query.filter(User.username == form.username.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user!")
        if user is None:
            raise ValidationError("Invalid user!")
        if not user.check_password(form.password.data):
            raise ValidationError("Invalid password!")

        # Make the current user available
        # to calling code.
        form.user = user


class BuyForm(FlaskForm):
    coin = TextAreaField('Coin', [validators.DataRequired()])

    def validate_coin(form, field):
        try:
            coindata = json.loads(form.coin.data)
        except:
            raise ValidationError("Json Error!")

        md5 = get_coin_MD5(coindata)
        try:
            spend = Spend.query.filter(Spend.md5 == md5).first()
        except:
            raise ValidationError("Database Error!")

        if spend is not None:
            raise ValidationError("Double spend attempt detected!")

        check_coin(coindata, current_user.username, sk_pem)

        form.md5 = md5
        form.am = coindata['AM']
