from datetime import datetime
import pymongo
import telebot
import os

# Inicializar bot
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Conexion con MongoDB
conn = pymongo.MongoClient(os.environ.get('DB_CONN'))
db = conn[os.environ.get('DB_DBNAME')]
coll = db[os.environ.get('DB_COLL')]

# Definición de métodos
def get_chatid(message):
	return message.chat.id

def count_chats_for_user(chat_id,user_id):
    return coll.count_documents({"ChatID": chat_id, "UserID": user_id})

def get_username_by_id(chat_id,user_id):
    result = coll.find({"ChatID": chat_id, "UserID": user_id}).limit(1)
    return result[0]["Username"]



def get_metrics_by_chat(message):
    users_id = coll.distinct("UserID", {"ChatID": get_chatid(message)})
    response = ""
    for id in users_id:
        usernames = get_username_by_id(get_chatid(message), id)
        users_logs = str(count_chats_for_user(get_chatid(message), id))
        response += "El usuario " + usernames + " ha enviado " + users_logs + " mensajes. \n"
    return response

def get_top_user_by_chat(message):
    users_id = coll.distinct("UserID", {"ChatID": get_chatid(message)})
    response = ""
    for id in users_id:
        usernames = get_username_by_id(get_chatid(message), id)
        users_logs = str(count_chats_for_user(get_chatid(message), id))
        response += "El usuario " + usernames + " ha sido el usuario más activo con " + users_logs + " mensajes. \n"
    return response

def insert_message_query(message):
    ts = (datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
    query = [{"UserID": message.from_user.id, "Username": message.from_user.username, "Date": ts, "ChatID": message.chat.id, "Text": message.text}]
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

@bot.message_handler(commands=['top_user'])
def top_user(message):
	bot.reply_to(message, get_top_user_by_chat(message))

@bot.message_handler(commands=['metrics'])
def metrics_users(message):
    bot.reply_to(message, get_metrics_by_chat(message))

@bot.message_handler(content_types=['text'])
def store_chat(message):
	insert_message_query(message)

bot.infinity_polling()