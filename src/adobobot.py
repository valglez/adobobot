from datetime import datetime
import mysql.connector
import pymongo
import telebot
import os

# Inicializar bot
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Conexión con el servidor MySQL Server
conn= mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    passwd=os.environ.get('DB_PASSWD'),
    db=os.environ.get('DB_DBNAME')
)

# Conexion con el servidor MongoDB
conn = pymongo.MongoClient(os.environ.get('DB_CONN'))
db = conn[os.environ.get('DB_DBNAME')]
coll = db[os.environ.get('DB_COLL')]

# Definición de métodos para MongoDB
def get_users():
    return coll.find()

# Definición de métodos para MariaDB
def get_chatid(message):
	return message.chat.id

def exec_query(query):
	cursor = conn.cursor()
	cursor.execute(query)
	result=cursor.fetchall()
	return result

def get_metrics_by_chat(message):
	cursor = conn.cursor()
	cursor.execute(f"SELECT Username, COUNT(UserID) FROM chat_log WHERE ChatID = {get_chatid(message)} GROUP BY UserID")
	result = cursor.fetchall()
	response = ""
	for row in result:
		user = row[0] or "Anonymous"
		response += "El usuario " + user + " ha enviado " + str(row[1]) + " mensajes. \n"
	return response

def get_top_user_by_chat(message):
	result = exec_query(f"SELECT Username, COUNT(*) AS Total FROM chat_log WHERE ChatID = {get_chatid(message)} GROUP BY Username ORDER BY Total DESC LIMIT 1")
	response=""
	for row in result:
		user = row[0] or "Anonymous"
		response += "El usuario " + user + " ha sido el usuario más activo con un total de " + str(row[1]) + " mensajes. \n"
	return response

def insert_message_query(message):
	cursor = conn.cursor()
	query = "INSERT INTO chat_log (UserID, Username, Date, ChatID, Text) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE UserID=VALUES(UserID), Username=VALUES(Username), Date=VALUES(Date), ChatID=VALUES(ChatID), Text=VALUES(Text)"
	ts=(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
	values = (message.from_user.id, message.from_user.username, ts, message.chat.id, message.text)
	cursor.execute(query, values)
	conn.commit()

def insert_message_query_mongo(message):
    ts = (datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
    query = [{"ChatID": message.from_user.id, "Username": message.from_user.username, "Date": ts, "ChatID": message.chat.id, "Text": message.text}]
    coll.insert_many(query)

# Definición de handlers para MongoDB
@bot.message_handler(commands=['users'])
def show_users_mongo(message):
    bot.reply_to(message, get_users())

@bot.message_handler(content_types=['text'])
def store_chat_mongo(message):
	insert_message_query_mongo(message)

# Definición de handlers para MariaDB
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
def metric_users(message):
	bot.reply_to(message, get_metrics_by_chat(message))

# Definición de handler para inserts para MariaDB y MongoDB
@bot.message_handler(content_types=['text'])
def store_chat(message):
	insert_message_query(message)

bot.infinity_polling()