from controllers import bot_controller
from database import mongo
from telegram import telegram
from cache import cache
import os

db = mongo.Database(os.environ.get('DB_CONN'), os.environ.get(
    'DB_NAME'), os.environ.get('DB_COL'))
users_cache = cache.Cache()
ctrl = bot_controller.BotControllers(db, users_cache)
bot = telegram.Bot(os.environ.get('BOT_TOKEN'), ctrl)
ctrl.load_users()
bot.start_handlers()
bot.start_polling()