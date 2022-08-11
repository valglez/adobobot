from datetime import datetime
import pymongo
import telebot
import os

# Inicializar bot
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Conexion con MongoDB
conn = pymongo.MongoClient(os.environ.get('DB_CONN'))
db = conn[os.environ.get('DB_NAME')]
coll = db[os.environ.get('DB_COL')]

# Definición de métodos
def get_chatid(message):
	return message.chat.id

def count_chats_for_user(chat_id, user_id):
    return coll.count_documents({"chatid": chat_id, "userid": user_id})

def get_username_by_id(chat_id, user_id):
    result = coll.find({"chatid": chat_id, "userid": user_id}).limit(1)
    return result[0]["name"] or "Anonymous"

def get_metrics_by_chat(message):
    users_id = coll.distinct("userid", {"chatid": get_chatid(message)})
    while users_id:
        response = ""
        for id in users_id:
            usernames = get_username_by_id(get_chatid(message), id)
            users_logs = str(count_chats_for_user(get_chatid(message), id))
            response += "El usuario " + usernames + " ha enviado " + users_logs + " mensajes. \n"
        return response
    else:
        response = "No se encontraron registros en este chat."
        return response

def insert_message_query(message):
    ts = (datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
    query = [{"userid": message.from_user.id, "name": message.from_user.username, "date": ts, "chatid": message.chat.id, "msgs": message.text}]
    coll.insert_many(query)

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
    bot.reply_to(message, get_metrics_by_chat(message))

@bot.message_handler(content_types=['text'])
def store_messages(message):
	insert_message_query(message)

# TO DO
# This handler doesn't work cause needs a definition to obtain the metric's output in dict format

@bot.message_handler(commands=['top_user'])
def users_metrics(message):
    bot.reply_to(message, get_metrics_by_chat(message))

bot.infinity_polling()