from ctfapp import bcrypt, db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # Data Model User Table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return self.id


class Spend(db.Model):
    # Data Model Spend
    id = db.Column(db.Integer, primary_key=True)
    md5 = db.Column(db.String(32))

    def __init__(self, md5):
        self.md5 = md5


class Coins(db.Model):
    # Data Model for Coins
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(120))
    coin = db.Column(db.Text())

    def __init__(self, coin, owner):
        self.coin = coin
        self.owner = owner


class Bought(db.Model):
    # Data Model for bought stuff
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    item = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self, user, item, amount):
        self.user = user
        self.item = item
        self.amount = amount

    def __repr__(self):
        return '<%r, %r, %r>' % (self.user, self.item, self.amount)
