from controllers import bot_controller
from database import mongo
from telegram import telegram
import os

db = mongo.Database(os.environ.get('DB_CONN'), os.environ.get(
    'DB_NAME'), os.environ.get('DB_COL'))
ctrl = bot_controller.BotControllers(db)
bot = telegram.Bot(os.environ.get('BOT_TOKEN'), ctrl)
bot.start_handlers()
bot.start_polling()
