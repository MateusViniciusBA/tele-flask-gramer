from bot.bot import TOKEN
import requests


def unban_user(channel_id, user_id):
    try:
        data = requests.get(f'https://api.telegram.org/bot{TOKEN}/unbanChatMember?chat_id={channel_id}&user_id={user_id}').json()
        if data['ok'] != True:
            print(f"Não foi possível desbanir o usuário, {data}")
        else:
            print(f"Usuário desbanido com sucesso, {data}")
    except:
        print("Não foi possível desbanir o usuário")
        pass