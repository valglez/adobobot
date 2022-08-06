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
    db='adobobot'
)

# Definición de handlers
@bot.message_handler(commands=['start'])
def top_user(message):
	cursor = conn.cursor()
	cursor.execute("SELECT Definition FROM bot_commands WHERE Command = 'start'")
	result=cursor.fetchall()
	bot.reply_to(message, result)

@bot.message_handler(commands=['help'])
def top_user(message):
	cursor = conn.cursor()
	cursor.execute("SELECT Definition FROM bot_commands WHERE Command = 'help'")
	result=cursor.fetchall()
	bot.reply_to(message, result)

@bot.message_handler(commands=['about'])
def top_user(message):
	cursor = conn.cursor()
	cursor.execute("SELECT Definition FROM bot_commands WHERE Command = 'about'")
	result=cursor.fetchall()
	bot.reply_to(message, result)

@bot.message_handler(commands=['top_user'])
def top_user(message):
	cursor = conn.cursor()
	cursor.execute("SELECT Username, COUNT(*) AS Total FROM chat_log GROUP BY Username ORDER BY Total DESC LIMIT 1")
	result=cursor.fetchall()
	bot.reply_to(message, result)

@bot.message_handler(commands=['metrics'])
def metric_users(message):
	cursor = conn.cursor()
	cursor.execute("SELECT Username, COUNT(UserID) FROM chat_log GROUP BY UserID")
	result = cursor.fetchall()
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