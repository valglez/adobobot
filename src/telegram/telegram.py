import telebot

class Bot:
    def __init__(self, token, controllers):
        self.bot = telebot.TeleBot(token)
        self.ctrl = controllers
        print('Started bot.')

    def get_chatid(self, message):
        return message.chat.id

    def get_userid(self, message):
        return message.from_user.id

    def get_chat_title(self, message):
        return message.chat.title

    def get_chat_text(self, message):
        return message.text

    def get_arg(self, arg):
        input = arg.split()[1:]
        if not input:
            limit = 10
            return limit
        elif str.isdigit(input[0]) == False:
            limit = 10
            return limit
        elif 1 <= int(input[0]) <= 10:
            limit = int(input[0])
            return limit
        elif int(input[0]) == 0 or int(input[0]) > 10:
            limit = 10
            return limit

    def start_handlers(self):

        @self.bot.message_handler(commands=['start'])
        def send_start(message):
            self.bot.reply_to(
                message, 'Escribe /help para mostrarte los comandos disponibles.')

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.bot.reply_to(
                message, 'Puedes usar los siguientes comandos:\n\n\
/top - Muestra el ranking de usuarios del chat. Ejemplo: /top 3\n\
/max - Muestra el usuario más activo del chat\n\
/metrics - Muestra el total de mensajes de los usuarios del chat\n\
/about - Sobre mí')

        @self.bot.message_handler(commands=['about'])
        def about_bot(message):
            self.bot.reply_to(
                message, 'Desarrollado por valglez @ https://github.com/valglez/adobobot')

        @self.bot.message_handler(commands=['metrics'])
        def users_metrics(message):
            self.bot.reply_to(message, self.ctrl.get_total_users_metrics_in_this_chat(self.get_chatid(message), self.get_userid(message), self.get_arg(self.get_chat_text(message))))

        @self.bot.message_handler(commands=['max'])
        def users_metrics(message):
            self.bot.reply_to(message, self.ctrl.get_top_user_metrics_in_this_chat(self.get_chatid(message), self.get_userid(message), 1))

        @self.bot.message_handler(commands=['top'])
        def users_metrics(message):
            self.bot.reply_to(message, self.ctrl.get_ranking_metrics_in_this_chat(self.get_chat_title(message), self.get_chatid(message), self.get_userid(message), self.get_arg(self.get_chat_text(message))))

        @self.bot.message_handler(content_types=['text'])
        def col_stores(message):
            self.ctrl.store_user(message.from_user.id,message.from_user.username)
            self.ctrl.store_msg(message.from_user.id,message.date,self.get_chatid(message),message.text)

    def start_polling(self):
        print('Started polling..')
        return self.bot.infinity_polling()