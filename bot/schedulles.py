from bot.bot import TOKEN, connection_db
from bot.database import *
from datetime import datetime
import requests
import json

def scheduller_ban():
    print("Run check user scheduler")
    purchases = json.loads(get_purchases(connection_db))
    for purchase in purchases:
        end_time = datetime.strptime(purchase['end_date'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        today = datetime.now()
        
        
        if purchase['order_status'] != 'approved' or purchase['order_status'] != 'active' or today.date() >= end_time.date():
            db_products = json.loads(get_product(connection_db, purchase['product']))
            if db_products:
                groups = db_products[0]['groups'].split(',')
                for group in groups:
                    db_groups = json.loads(get_group(connection_db, group))
                    try:
                        chat_id = db_groups[0]['chat_id']
                        data = requests.get(f'https://api.telegram.org/bot{TOKEN}/banChatMember?chat_id={chat_id}&user_id={purchase["telegram_id"]}').json()
                        if data['ok'] != True:
                            print(f"Não foi possível banir o usuário, {data}")
                        else:
                            print(f"Usuário banido com sucesso, {data}")
                    except:
                        print("Não foi possível banir o usuário")
                        pass
            