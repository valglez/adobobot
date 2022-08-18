from datetime import datetime, timedelta
from telebot import telebot
import pymongo
import os

# Inicializar bot
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Conexion con MongoDB
conn = pymongo.MongoClient(os.environ.get('DB_CONN'))
db = conn[os.environ.get('DB_NAME')]
col = db[os.environ.get('DB_COL')]

# Definición de métodos
def get_chatid(message):
	return message.chat.id

def get_userid(message):
	return message.from_user.id

def get_chat_title(message):
	return message.chat.title

def get_chat_text(message):
    return message.text

def get_input(arg):
    input = arg.split()[1:]
    if not input:
        limit = 10
        return limit
    elif str.isdigit(input[0]) == False:
        limit = 10
        return limit
    elif 1 <= int(input[0]) <= 10:
        limit = int(input[0])
        return limit
    elif int(input[0]) == 0 or int(input[0]) > 10:
        limit = 10
        return limit

def check_user(chat_id, user_id):
    return col.count_documents({'chatid': chat_id, 'userid': user_id})

def get_sorted_metrics_by_chatid(message):
    pipeline = (
        {'$match':{'chatid': get_chatid(message)}},
        {'$group':{'_id':'$name','msgs':{'$sum': 1}}},
        {'$sort':{'msgs':-1}},
        {'$limit':(get_input(get_chat_text(message)))})
    return col.aggregate(list(pipeline))

def get_top_user_metrics_by_chatid(message):
    pipeline = (
        {'$match':{'chatid': get_chatid(message)}},
        {'$group':{'_id':'$name','msgs':{'$sum': 1}}},
        {'$sort':{'msgs':-1}},
        {'$limit':1})
    return col.aggregate(list(pipeline))

def get_ranking_metrics_in_this_chat(message):
    if check_user(get_chatid(message),get_userid(message)):
        chat_title = get_chat_title(message) or 'este chat'
        response = 'TOP de mensajes en ' +  chat_title + ':\n'
        for idx, id in enumerate(get_sorted_metrics_by_chatid(message)):
            name = id['_id'] or 'Anonymous'
            idx += 1
            if idx == 1:
                response += str(idx) + '. ' + name + ' (' + str(id['msgs']) + ') ' + str('🥇') + '\n'
            elif idx == 2:
                response += str(idx) + '. ' + name + ' (' + str(id['msgs']) + ') ' + str('🥈') + '\n'
            else:
                response += str(idx) + '. ' + name + ' (' + str(id['msgs']) + ') ' + str('🥉') + '\n'
        return response
    else:
        response = 'Sin registros.'
        return response

def get_total_users_metrics_in_this_chat(message):
    if check_user(get_chatid(message),get_userid(message)):
        response = ''
        for id in get_sorted_metrics_by_chatid(message):
            name = id['_id'] or 'Anonymous'
            response += '• ' + name + ' ha escrito un total de ' + str(id['msgs']) + ' mensajes.\n'
        return response
    else:
        response = 'Sin registros.'
        return response

def get_top_user_metrics_in_this_chat(message):
    if check_user(get_chatid(message),get_userid(message)):
        response = ''
        for id in get_top_user_metrics_by_chatid(message):
            name = id['_id'] or 'Anonymous'
            response += name + ' ha sido el usuario más activo con un total de ' + str(id['msgs']) + ' mensajes.'
        return response
    else:
        response = 'Sin registros.'
        return response

def store_logs(message):
    currdate = (datetime.fromtimestamp(message.date) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    col.insert_many( [
        {'userid': message.from_user.id,
        'name': message.from_user.username,
        'date': currdate,
        'chatid': message.chat.id,
        'msgs': message.text}
    ] )

#Definición de handlers
@bot.message_handler(commands=['start'])
def start_bot(message):
    response = 'Escribe /help para mostrarte los comandos disponibles.'
    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def help_bot(message):
    response = 'Puedes usar los siguientes comandos:\n\n\
/ranking - Muestra el ranking de usuarios del chat\n\
/metrics - Muestra el total de mensajes de los usuarios del chat\n\
/top_user - Muestra el usuario más activo del chat\n\
/about - Sobre mí'
    bot.reply_to(message, response)

@bot.message_handler(commands=['about'])
def about_bot(message):
    response = 'Desarrollado por valglez @ https://github.com/valglez'
    bot.reply_to(message, response)

@bot.message_handler(commands=['metrics'])
def send_all_users_metrics_in_this_chat(message):
    bot.reply_to(message, get_total_users_metrics_in_this_chat(message))

@bot.message_handler(commands=['top_user'])
def send_top_user_metrics_in_this_chat(message):
    bot.reply_to(message, get_top_user_metrics_in_this_chat(message))

@bot.message_handler(commands=['ranking'])
def send_top_user_metrics_in_this_chat(message):
    bot.reply_to(message, get_ranking_metrics_in_this_chat(message))

@bot.message_handler(content_types=['text'])
def store_logs_in_this_chat(message):
	store_logs(message)

bot.infinity_polling()