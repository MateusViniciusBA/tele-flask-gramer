from flask import Blueprint, request, jsonify, Response, render_template, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user

import json

from app.app import bot
from app.models import *
from app.forms import *

cpanel_bp = Blueprint('cpanel', __name__, url_prefix='/cpanel')

@login_required
@cpanel_bp.route('/')
def index():
    return render_template('index.html', segment='index')

#AUTHENTICATION

@cpanel_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('cpanel.index'))

    if login_form.validate_on_submit():
        print("Validated")
        email = login_form.email.data
        password = login_form.password.data

        user = Admin.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return render_template('index.html', user=user)
        else:
            return render_template('login.html', msg='Invalid email or password', form=login_form)
    else:
        return render_template('login.html', form=login_form)

@cpanel_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cpanel.login'))

@cpanel_bp.route('/register', methods=['GET', 'POST'])
def register():

    register_form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('cpanel.index'))

    if register_form.validate_on_submit():
        print("Validated")
        email = register_form.email.data
        password = register_form.password.data
        confirm_password = register_form.confirm_password.data

        if password != confirm_password:
            return render_template('login.html', form=register_form, msg='Passwords do not match')

        user = Admin.query.filter_by(email=email).first()

        if user:
            return render_template('register.html', form=register_form, msg='Email already exists')

        user = Admin(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return render_template('login.html', form=register_form, msg=f"Registration successful please <a href='{{url_for('cpanel.login')}}'>Login Here</a>")
    else:
        return render_template('register.html', form=register_form)


#PRODUCTS

@cpanel_bp.route('/product')
@login_required
def product():
    products = Product.query.all()
    groups = Telegram_Group.query.all()
    return render_template('products.html', products=products, telegram_groups=groups, segment='product')

@cpanel_bp.route('/product/add', methods=['POST'])
@login_required
def add_product():
    reqst_data = request.get_json()
    groups_json = ""
    for group in reqst_data['groups']:
        groups_json += group + "," if group != reqst_data['groups'][-1] else group

    name = reqst_data['name']
    groups = groups_json
    platform_name = reqst_data['platform']
    platform_id = reqst_data['platform_id']
    duration = reqst_data['duration']
    check_product = Product.query.filter_by(platform_id=platform_id).first()

    if check_product:
        return jsonify({'status': 'error', 'msg': 'Product already exists'})
    
    product = Product(name=name, groups=groups, platform_name=platform_name, platform_id=platform_id, duration=duration)
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'status': 'ok', 'msg': 'Product Added'})

@cpanel_bp.route('/product/remove/<id>')
@login_required
def remove_product(id):

    product = Product.query.filter_by(id=id).first()

    db.session.delete(product)
    db.session.commit()
    
    return "ok"
   

#PURCHASES

@cpanel_bp.route('/purchase')
@login_required
def purchase():
    purchases = Purchase.query.all()
    products = Product.query.all()
    return render_template('purchases.html', purchases=purchases, products=products, segment='purchase')

@cpanel_bp.route('/purchase/add', methods=['POST'])
@login_required
def add_purchase():
    reqst_data = request.get_json()
    buyer_email = reqst_data['buyer_mail']
    product_name = reqst_data['product']
    order_token = reqst_data['token']


    product = Product.query.filter_by(name=product_name).first()
    if not product:
        return jsonify({'status': 'error', 'msg': 'Product does not exist'})

    duration = product.duration

    purchase = Purchase(buyer_email=buyer_email, product=product_name , order_token=order_token, duration=duration, order_status="APPROVED")
    db.session.add(purchase)
    db.session.commit()

    return jsonify({'status': 'ok', 'msg': 'Purchase Added'})

@cpanel_bp.route('/purchase/remove/<id>')
@login_required
def remove_purchase(id):
    
        purchase = Purchase.query.filter_by(id=id).first()
    
        db.session.delete(purchase)
        db.session.commit()
        
        return "ok" 


#TELEGRAM GROUPS

@cpanel_bp.route('/telegram')
@login_required
def telegram():
    groups = Telegram_Group.query.all()
    return render_template('telegram.html', telegram_groups=groups, segment='telegram')

@cpanel_bp.route('/telegram/add', methods=['POST'])
@login_required
def add_telegram():

    channel_name = request.form['group_name']
    if not "@" in channel_name:
        return jsonify({'status': 'error', 'msg': 'Invalid Link, please enter a @telegram_group_name'}), 400

    try:
        group_data = json.loads(bot.get_chat(chat_id=channel_name).to_json())
    except Exception as e:
        return jsonify({'status': 'error', 'msg': f'{e}'}), 400

    channel_id = group_data['id']
    channel_title = group_data['title']
    channel_username = group_data['username']


    telegram_group = Telegram_Group(link=channel_username, name=channel_title, chat_id=channel_id)
    db.session.add(telegram_group)
    db.session.commit()
    return jsonify({'status': 'ok', 'msg': 'Telegram Group Added'})
    
@cpanel_bp.route('/telegram/remove/<id>')
@login_required
def remove_telegram(id):
    
    telegram_group = Telegram_Group.query.filter_by(id=id).first()
    if not telegram_group:
        return jsonify({'status': 'error', 'msg': 'Group does not exist'}), 400

    db.session.delete(telegram_group)
    db.session.commit()
    return "ok"







