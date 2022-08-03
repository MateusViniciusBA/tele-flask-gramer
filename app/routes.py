from app.app import app
from app.models import *
from app.utils import unban_user

from flask import redirect, request, Blueprint, url_for

app_bp = Blueprint('app', __name__)

TOKEN = app.config['BOT_TOKEN']
 
@app_bp.route('/')
def index():
    return redirect(url_for('cpanel.index'))

@app_bp.route('/webhooks/hotmart', methods=['POST'])
def webhooks_hotmart():
    data = request.get_json(force=True)
    event = data['event']

    if 'PURCHASE_APPROVED' in event:
        order_token = data['data']['purchase']['transaction']
        buyer_email = data['data']['buyer']['email']
        product_id = data['data']['product']['id']
        status = data['data']['purchase']['status']

        product = Product.query.filter_by(platform_id=product_id).first()
        if not product:
            return "Product does not exist"
        product_name = product.name
        duration = product.duration

        check_purchase = Purchase.query.filter_by(order_token=order_token).first()
        if check_purchase:
            
            products = Product.query.filter_by(name=check_purchase.product).first()
            if products:
                groups = products.groups.split(',')
                for group in groups:
                    print(group)
                    group_data = Telegram_Group.query.filter_by(name=group).first()
                    if group_data:
                        group_id = group_data.chat_id
                        unban_user(group_id, check_purchase.telegram_id)
                        print("Usuário desbaneado")
                        
            check_purchase.order_status = status
            check_purchase.buyer_email = buyer_email
            check_purchase.product = product_name
            check_purchase.duration = duration
            check_purchase.product_name = product_name
            check_purchase.set_end_date(duration)
            db.session.commit()
            return "Purchase approved"
        
        purchase = Purchase(buyer_email=buyer_email, product=product_name, duration=duration, order_token=order_token, order_status="approved")
        db.session.add(purchase)
        db.session.commit()
        return "Purchase approved"

    elif 'PURCHASE_REFUNDED' in event:
        order_token = data['data']['purchase']['transaction']
        status = data['data']['purchase']['status']

        purchase = Purchase.query.filter_by(order_token=order_token).first()
        if purchase:
            purchase.order_status = status
            db.session.commit()
            return "ok"
        else:
            return "purchase not found"

    elif 'PURCHASE_DELAYED' in event:
        order_token = data['data']['purchase']['transaction']
        status = data['data']['purchase']['status']

        purchase = Purchase.query.filter_by(order_token=order_token).first()
        if purchase:
            purchase.order_status = status
            db.session.commit()
            return "ok"
        else:
            return "purchase not found"
    
    elif 'PURCHASE_CANCELED' in event:
        order_token = data['data']['purchase']['transaction']
        status = data['data']['purchase']['status']

        purchase = Purchase.query.filter_by(order_token=order_token).first()
        if purchase:
            purchase.order_status = status
            db.session.commit()
            return "ok"
        else:
            return "purchase not found"


@app_bp.route('/webhooks/braip', methods=['POST'])
def webhooks_braip():
    pass

@app_bp.route('/webhooks/kiwify', methods=['POST'])
def webhooks_kiwify():

    data = request.get_json(force=True)

    order_token = data['Subscription']['id']
    order_status = data['Subscription']['status']
    product_id = data['Subscription']['plan']['id']
    buyer_email = data['Customer']['email']

    product = Product.query.filter_by(platform_id=product_id).first()
    if not product:
        return "Product does not exist"
    product_name = product.name
    duration = product.duration

    check_purchase = Purchase.query.filter_by(order_token=order_token).first()
    if check_purchase:
        check_purchase.order_status = order_status
        check_purchase.buyer_email = buyer_email
        check_purchase.product = product_name
        check_purchase.duration = duration
        check_purchase.product_name = product_name
        check_purchase.set_end_date(duration)
        db.session.commit()
        return "Purchase approved"
    else:
        purchase = Purchase(buyer_email=buyer_email, product=product_name, duration=duration, order_token=order_token, order_status=order_status)
        db.session.add(purchase)
        db.session.commit()
        return "Purchase approved"
