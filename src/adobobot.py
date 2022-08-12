from datetime import datetime
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
    return col.count_documents({"chatid": chat_id, "userid": user_id})

def get_username_by_id(chat_id, user_id):
    result = col.find({"chatid": chat_id, "userid": user_id})
    return result[0]["name"] or "Anonymous"

def get_total_metrics_in_logs(message):
    result = col.distinct("userid", {"chatid": get_chatid(message)})
    return result

def get_metrics_by_chat(message):
    mylist = []
    users_id = get_total_metrics_in_logs(message)
    for id in users_id:
        usernames = get_username_by_id(get_chatid(message), id)
        user_chats = count_chats_for_user(get_chatid(message), id)
        keys = ["username", "msgs"]
        values = [usernames, user_chats]
        mydict = dict(zip(keys, values))
        mylist.append(mydict)
    return mylist

def get_metrics_for_all_users_by_chat(message):
    users_id = get_metrics_by_chat(message)
    if users_id:
        response = ""
        for id in users_id:
            response += "El usuario " + id["username"] + " ha escrito un total de " + str(id["msgs"]) + " mensajes. \n"
        return response
    else:
        response = "No se encontraron registros en este chat."
        return response

def get_top_metrics_user_by_chat(message):
    users_id = get_metrics_by_chat(message)
    if users_id:
        response = ""
        for id in users_id:
            max_msgs = max(id["msgs"])
            print(max_msgs)
            response += "El usuario " + id["username"] + " ha sido el usuario más activo con un total de " + str(max_msgs) + " mensajes. \n"
        return response
    else:
        response = "No se encontraron registros en este chat."
        return response

def insert_message_query(message):
    ts = (datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
    query = [{"userid": message.from_user.id, "name": message.from_user.username, "date": ts, "chatid": message.chat.id, "msgs": message.text}]
    col.insert_many(query)

#Definición de handlers
@bot.message_handler(commands=['start'])
def send_start(message):
	bot.reply_to(message, 'Hola, mi nombre es adobobot. Escribe /help para mostrarte los comandos disponibles.')

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, 'Estos son los comandos que puedes utilizar:\n\n/start - Iniciar el bot\n/top_user - Usuario más activo\n/metrics - Muestra el total de mensajes de usuarios del grupo\n/about - Sobre mí')

@bot.message_handler(commands=['about'])
def about_bot(message):
	bot.reply_to(message, 'Developed by valglez @ https://github.com/valglez')

@bot.message_handler(commands=['metrics'])
def users_metrics(message):
    bot.reply_to(message, get_metrics_for_all_users_by_chat(message))

@bot.message_handler(commands=['top_user'])
def users_metrics(message):
    bot.reply_to(message, get_top_metrics_user_by_chat(message))

@bot.message_handler(content_types=['text'])
def store_messages(message):
	insert_message_query(message)

bot.infinity_polling()