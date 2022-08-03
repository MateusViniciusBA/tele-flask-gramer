from app.app import db, login_manager

from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

#Models for database

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True)
    password = db.Column(db.String(180))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = generate_password_hash(value)

            setattr(self, property, value)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Admin %r>' % self.username

class Purchase(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    buyer_email = db.Column(db.String(180))
    product = db.Column(db.Integer)
    buy_date = db.Column(db.DateTime, default=datetime.now)
    duration = db.Column(db.String(180))
    end_date = db.Column(db.DateTime)
    order_token = db.Column(db.String(80), unique=True)
    order_status = db.Column(db.String(80))
    telegram_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'duration':
                if value == 'test':
                    self.end_date = datetime.now() + timedelta(hours=2)
                    value = '2 Horas'
                elif value == '7days':
                    self.end_date = datetime.now() + timedelta(days=7)
                    value = '7 Dias'
                elif value == '1month':
                    self.end_date = datetime.now() + timedelta(days=30)
                    value = '1 Mês'
                elif value == '3month':
                    self.end_date = datetime.now() + timedelta(days=90)
                    value = '3 Meses'
                elif value == '6month':
                    self.end_date = datetime.now() + timedelta(days=180)
                    value = '6 Meses'
                elif value == '1year':
                    self.end_date = datetime.now() + timedelta(days=365)
                    value = '1 Ano'
                elif value == 'vitality':
                    self.end_date = datetime.now() + timedelta(days=365*999)
                    value = 'Vitalício'

            setattr(self, property, value)

    def set_end_date(self, duration):
        if duration == 'test':
            self.end_date = datetime.now() + timedelta(hours=2)
        elif duration == '7days':
            self.end_date = datetime.now() + timedelta(days=7)
        elif duration == '1month':
            self.end_date = datetime.now() + timedelta(days=30)
        elif duration == '3month':
            self.end_date = datetime.now() + timedelta(days=90)
        elif duration == '6month':
            self.end_date = datetime.now() + timedelta(days=180)
        elif duration == '1year':
            self.end_date = datetime.now() + timedelta(days=365)
        elif duration == 'vitality':
            self.end_date = datetime.now() + timedelta(days=365*999)

    def __repr__(self):
        return '<Purchase %r>' % self.order_token

class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    platform_id = db.Column(db.Integer)
    platform_name = db.Column(db.String(80))
    duration = db.Column(db.String(180), nullable=False)
    groups = db.Column(db.Text())
    add_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return '<Product %r>' % self.name

class Telegram_Group(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    chat_id = db.Column(db.Integer)
    link = db.Column(db.String(180))
    add_att = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return '<Telegram_Group %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))
