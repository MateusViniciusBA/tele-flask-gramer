import json
import re
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ParseMode
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import Default_Config
from bot.database import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = Default_Config.BOT_TOKEN
scheduller = BackgroundScheduler(daemon=True, timezone='America/Sao_Paulo')
connection_db = make_connection()
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

msg_wellcome = "Bem-vindo ao bot do grupo de compra!\nPor favor digite seu email para fazer a autenticação."

def cancel(update, context):
    """End conversation."""
    update.message.reply_text('Bye!')
    return ConversationHandler.END

def get_email(update, context):
    """Get email from user."""
    email = update.message.text
    regex1 = re.compile('[\w.]+\@\w+\.\w+\.\w+')
    regex2 = re.compile('[\w.]+\@\w+\.\w+')
    if regex1.finditer(email) or regex2.finditer(email):
        check = json.loads(get_purchase_by_email(connection_db,email))
        if check:
            user_id = update.message.from_user.id
            msg = f"Bem-vindo <b>{check[0]['buyer_email']}</b> !\n"
            groups_links = []
            
            for purchase in check:

                update_purchase_telegram_id(connection_db, purchase['order_token'], user_id)
                db_products = json.loads(get_product(connection_db, purchase['product']))
                if db_products:
                    groups = db_products[0]['groups'].split(',')

                    for group in groups:
                        
                        if purchase['order_status'] == 'APPROVED':
                            db_groups = json.loads(get_group(connection_db, group))
                            try:
                                group_link = context.bot.create_chat_invite_link(db_groups[0]['chat_id'], member_limit=1)['invite_link']
                            except:
                                group_link = 'Não foi possível criar o link do grupo'
                            groups_links.append({'product': purchase['product'],'group': group, 'link': group_link})
                        else:
                            groups_links.append({'product': purchase['product'],'group': group, 'link': 'Pagamento não aprovado'})

            for group in groups_links:
                msg += f"<b>{group['product']}</b> - <b>{group['group']}</b> - {group['link']}\n"
            
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.HTML)
            msg = ""
            return ConversationHandler.END
        else:
            update.message.reply_text('You are now subscribed!')
            return ConversationHandler.END
    else:
        update.message.reply_text('Please enter a valid email!')
        return 1

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(msg_wellcome)
    return 1

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    dp.add_error_handler(error)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, get_email)],
        },
        fallbacks=[CommandHandler('stop', cancel)]
    )

    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(conversation_handler)

    from bot.schedulles import scheduller_ban
    scheduller.add_job(scheduller_ban, 'interval', seconds=10)
    scheduller.start()
    
    updater.start_polling()

    updater.idle()
