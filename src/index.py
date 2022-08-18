from controllers import BookController
from database import Database
from telegram import Bot
import os

db = Database(os.environ.get('DB_CONN'), os.environ.get('DB_NAME'), os.environ.get('DB_COL'))
ctrl = BookController(db.connect())
bot = Bot(os.environ.get('BOT_TOKEN'), ctrl)
bot.start_polling()