import telebot
import os
import mysql.connector
from datetime import datetime

# Inicializar bot
bot = telebot.TeleBot(os.environ.get('bot_token'))

# Conexión con el servidor MySQL Server
conn= mysql.connector.connect(
    host=os.environ.get('host'),
    user=os.environ.get('user'),
    passwd=os.environ.get('mysqlpass'),
    db='adobobot'
)

# Definición de handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Hola, mi nombre es adobobot. Escribe /help para mostrarte los comandos disponibles.')

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, 'Estos son los comandos que puedes utilizar:\n\n/start - Iniciar el bot\n/top_user - Usuario más activo\n/about - Sobre mí')

@bot.message_handler(commands=['about'])
def send_about(message):
	bot.reply_to(message, 'Developed by valglez @ https://github.com/valglez')

@bot.message_handler(commands=['top_user'])
def top_user(message):
	cursor = conn.cursor()
	cursor.execute("SELECT Username, COUNT(*) AS Total FROM chat_log GROUP BY Username ORDER BY Total DESC LIMIT 1")
	result=cursor.fetchall()
	bot.reply_to(message, result)

@bot.message_handler(content_types=['text'])
def store_chat(message):
	cursor = conn.cursor()
	query = "INSERT INTO chat_log (UserID, Username, Date, ChatID, Text) VALUES (%s, %s, %s, %s, %s)"
	ts=(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
	values = (message.from_user.id, message.from_user.username, ts, message.chat.id, message.text)
	cursor.execute(query, values)
	conn.commit()

bot.infinity_polling()