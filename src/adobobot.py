from datetime import datetime, timedelta
import pymongo
import telebot
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

def count_chats_for_user(chat_id, user_id):
    return col.count_documents({'chatid': chat_id, 'userid': user_id})

def get_user_by_id(chat_id, user_id):
    result = col.find({'chatid': chat_id, 'userid': user_id})
    return result[0]['name'] or 'Anonymous'

def get_total_users_metrics(message):
    return col.distinct('userid', {'chatid': get_chatid(message)})

def get_ranked_metrics_by_chatid(message):
    pipeline = (
        {"$match":{"chatid":message.chat.id }},
        {"$group":{"_id":"$name","msgs":{"$sum": 1}}},
        {"$sort":{"msgs":-1}},{"$limit": 3}
    )
    users_metrics = col.aggregate(list(pipeline))
    response = 'Top de mensajes en este chat:\n\n'
    for id in users_metrics:
        name = id['_id'] or 'Anonymous'
        response += name + ' (' + str(id['msgs']) + ')\n'
    return response
        

def get_total_users_metrics_by_chat(message):
    mylist = []
    users_id = get_total_users_metrics(message)
    for id in users_id:
        username = get_user_by_id(get_chatid(message), id)
        user_chats = count_chats_for_user(get_chatid(message), id)
        mydict = {}
        mydict['name'] = username
        mydict['msgs'] = user_chats
        mylist.append(mydict)
    return mylist

def get_top_user_metrics_by_chat(message):
    users_metrics = get_total_users_metrics_by_chat(message)
    top_dict = {}
    max_value = max(users_metrics, key=lambda x:x['msgs'])
    top_dict = max_value
    return top_dict

def get_total_users_metrics_in_this_chat(message):
    users_id = get_total_users_metrics_by_chat(message)
    if users_id:
        response = ''
        for id in users_id:
            response += 'El usuario ' + id['name'] + ' ha escrito un total de ' + str(id['msgs']) + ' mensajes. \n'
        return response
    else:
        response = 'No se encontraron registros en este chat.'
        return response

def get_top_user_metrics_in_this_chat(message):
    users_metrics = get_total_users_metrics_by_chat(message)
    if users_metrics:
        top = get_top_user_metrics_by_chat(message)
        response = 'El usuario ' + top['name'] + ' ha sido el usuario más activo con un total de ' + str(top['msgs']) + ' mensajes. \n'
        return response
    else:
        response = 'No se encontraron registros en este chat.'
        return response

def store_logs(message):
    currdate = (datetime.fromtimestamp(message.date) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    query = [
        {'userid': message.from_user.id,
        'name': message.from_user.username,
        'date': currdate,
        'chatid': message.chat.id,
        'msgs': message.text}
    ]
    col.insert_many(query)

#Definición de handlers
@bot.message_handler(commands=['start'])
def start_bot(message):
    response = 'Escribe /help para mostrarte los comandos disponibles.'
    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def help_bot(message):
    response = 'Puedes usar los siguientes comandos:\n\n\
/top_user - Muestra el usuario más activo del chat\n\
/metrics - Muestra el total de mensajes de los usuarios del chat\n\
/about - Sobre mí'
    bot.reply_to(message, response)

@bot.message_handler(commands=['about'])
def about_bot(message):
    response = 'Desarrollado por valglez @ https://github.com/valglez'
    bot.reply_to(message, response)

@bot.message_handler(commands=['metrics'])
def send_all_users_metrics_in_this_chat(message):
    response = get_total_users_metrics_in_this_chat(message)
    bot.reply_to(message, response)

@bot.message_handler(commands=['top_user'])
def send_top_user_metrics_in_this_chat(message):
    response = get_top_user_metrics_in_this_chat(message)
    bot.reply_to(message, response)

@bot.message_handler(commands=['top3'])
def send_top_user_metrics_in_this_chat(message):
    response = get_ranked_metrics_by_chatid(message)
    bot.reply_to(message, response)

@bot.message_handler(content_types=['text'])
def store_logs_in_this_chat(message):
	store_logs(message)

bot.infinity_polling()