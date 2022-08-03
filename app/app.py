from app.config import Default_Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


import telegram

app  = Flask(__name__)
app.config.from_object(Default_Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'cpanel.login'

bot = telegram.Bot(token=app.config['BOT_TOKEN'])

from app.routes import app_bp
from app.cpanel.routes import cpanel_bp
app.register_blueprint(app_bp)
app.register_blueprint(cpanel_bp)

from app.models import *

@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    return date.strftime('%d/%m/%Y %H:%M')

@app.template_filter('statusFormat')
def _jinja2_filter_status(status):
    if status == 'DELAYED':
        return 'Atrasado'
    elif status == 'APPROVED':
        return 'Aprovado'
    elif status == 'CANCELED':
        return 'Cancelado'
    elif status == 'REFUNDED':
        return 'Reembolsado'
    else:
        return 'Desconhecido'

@app.template_filter('durationFormat')
def _jinja2_filter_duration(duration):
    if duration == 'test':
        return 'Teste'
    elif duration == '7days':
        return '7 dias'
    elif duration == '1month':
        return '1 mês'
    elif duration == '3month':
        return '3 meses'
    elif duration == '6month':
        return '6 meses'
    elif duration == '1year':
        return '1 ano'
    elif duration == 'vitality':
        return 'Vitalício'

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(type(message))

    return dict(mdebug=print_in_console)

@app.before_first_request
def before_first_request():
    db.create_all()

