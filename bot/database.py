import sqlalchemy as db
import json

metadata = db.MetaData()

def make_connection():
    engine = db.create_engine('sqlite:///app/debug.db', echo=False, connect_args={'check_same_thread': False})
    connection = engine.connect()
    return connection

def get_purchase_by_token(conn, order_token):
    purchase = conn.execute("SELECT * FROM purchase WHERE order_token = '%s'" % order_token).fetchall()
    return json.dumps( [dict(ix) for ix in purchase] )

def get_purchase_by_email(conn, email):
    purchase = conn.execute("SELECT * FROM purchase WHERE buyer_email = '%s'" % email).fetchall()
    return json.dumps( [dict(ix) for ix in purchase] )

def get_purchases(conn):
    purchases = conn.execute("SELECT * FROM purchase").fetchall()
    return json.dumps( [dict(ix) for ix in purchases] )

def get_product(conn, product_name):
    product = conn.execute("SELECT * FROM product WHERE name = '%s'" % product_name).fetchall()
    return json.dumps( [dict(ix) for ix in product] )

def get_products(conn):
    products = conn.execute("SELECT * FROM product").fetchall()
    return json.dumps( [dict(ix) for ix in products] )

def get_group(conn, group_title):
    group = conn.execute("SELECT * FROM telegram__group WHERE name = '%s'" % group_title).fetchall()
    return json.dumps( [dict(ix) for ix in group] )

def update_purchase_telegram_id(conn, order_token, telegram_id):
    conn.execute("UPDATE purchase SET telegram_id = '%s' WHERE order_token = '%s'" % (telegram_id, order_token))
    return True