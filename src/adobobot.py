from datetime import datetime
import mysql.connector
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

# Definición de métodos
def get_chatid(message):
	return message.chat.id

def get_metrics_by_chat(message):
	cursor = conn.cursor()
	cursor.execute(f"SELECT Username, COUNT(UserID) FROM chat_log WHERE ChatID = {get_chatid(message)} GROUP BY UserID")
	result = cursor.fetchall()
	response = ""
	for row in result:
		user = row[0] or "Anonymous"
		response += "El usuario " + user + " ha enviado " + str(row[1]) + " mensajes. \n"
	return response

def exec_select_query(query):
	cursor = conn.cursor()
	cursor.execute(query)
	result=cursor.fetchall()
	return result

def get_top_user_by_chat(message):
	result = exec_select_query(f"SELECT Username, COUNT(*) AS Total FROM chat_log WHERE ChatID = {get_chatid(message)} GROUP BY Username ORDER BY Total DESC LIMIT 1")
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

# Definición de handlers
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

@bot.message_handler(content_types=['text'])
def store_chat(message):
	insert_message_query(message)

bot.infinity_polling()