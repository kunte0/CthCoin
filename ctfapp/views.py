from flask import request, render_template, flash, redirect, abort
from flask import url_for, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from ctfapp import db, app, login_manager, sk_pem
from .forms import LoginForm, RegistrationForm, BuyForm
from .model import User, Spend, Coins, Bought
from .util import build_coin


ITEM = [[0, 'An AWSOME Gif', 5],
        [1, 'Useless Stuff', 30],
        [2, 'The FLAG', 120]]

login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')


@app.errorhandler(401)
def custom_401(error):
    flash('You have to login to view this page.')
    return redirect(url_for('index'))


@app.route('/')
def index():
    if not current_user.is_authenticated:
        flash('Welcome. \
            Feel free to register to recieve your first few CthCoins.')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        flash('Logged in successfully.')
        return redirect(url_for('profile'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        user = User(username, form.password.data)
        coin1 = Coins(build_coin(username, sk_pem, 5), username)
        coin2 = Coins(build_coin(username, sk_pem, 10), username)
        coin3 = Coins(build_coin(username, sk_pem, 50), username)
        db.session.add(user)
        db.session.add(coin1)
        db.session.add(coin2)
        db.session.add(coin3)
        db.session.commit()
        flash('Thanks for registering.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/wallet')
@login_required
def wallet():
    coins = Coins.query.filter(Coins.owner == current_user.username)
    return render_template('wallet.html', coins=coins)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/debugcoins')
@login_required
def debugcoins():
    spend = Spend.query.order_by(Spend.id.desc()).limit(50).all()
    return render_template('debug.html', spend=spend)


@app.route('/buy/<int:id>', methods=['GET', 'POST'])
@login_required
def buy(id):
    form = BuyForm(request.form)
    if id not in [0, 1, 2]:
        return abort(404)

    dbitem = Bought.query.filter(
        Bought.user == current_user.username).filter(Bought.item == id).first()

    send = 0
    if dbitem is not None:
        send = dbitem.amount

    item = ITEM[id]

    if send >= item[2]:
        flash('Thank you for your purchase.')
        return redirect(url_for('secret', id=id))

    if form.validate_on_submit():
        spend = Spend(form.md5)
        if dbitem is None:
            bought = Bought(current_user.username, id,
                            int(form.am))
            db.session.add(bought)
        else:
            dbitem.amount += int(form.am)

        db.session.add(spend)
        db.session.commit()
        return redirect(url_for('buy', id=id))

    return render_template('buy.html', form=form, item=item, send=send)


@app.route('/secret/<int:id>', methods=['GET', 'POST'])
@login_required
def secret(id):
    if id not in [0, 1, 2]:
        return abort(404)

    dbitem = Bought.query.filter(
        Bought.user == current_user.username).filter(Bought.item == id).first()

    send = 0
    if dbitem is not None:
        send = dbitem.amount

    item = ITEM[id]
    if send < item[2]:
        return redirect(url_for('profile'))

    return render_template('secret.html', id=id)


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template('shop.html')
