import telebot


class Bot:
    def __init__(self, token, controllers):
        self.bot = telebot.TeleBot(token)
        self.ctrl = controllers

    def get_chatid(self, message):
        return message.chat.id

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
                message, 'Hola, mi nombre es adobobot. Escribe /help para mostrarte los comandos disponibles.')

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.bot.reply_to(
                message, 'Estos son los comandos que puedes utilizar:\n\n/start - Iniciar el bot\n/top_user - Usuario más activo\n/metrics - Muestra el total de mensajes de usuarios del grupo\n/about - Sobre mí')

        @self.bot.message_handler(commands=['about'])
        def about_bot(message):
            self.bot.reply_to(
                message, 'Developed by valglez @ https://github.com/valglez')

        @self.bot.message_handler(commands=['metrics'])
        def users_metrics(message):
            self.bot.reply_to(message, self.ctrl.get_total_users_metrics_in_this_chat(self.get_chatid()))

        @self.bot.message_handler(content_types=['text'])
        def store_messages(message):
            self.ctrl.store_msg(message)

        # TO DO
        # This handler doesn't work cause needs a definition to obtain the metric's output
        # in dict format

        @self.bot.message_handler(commands=['top_user'])
        def users_metrics(message):
            self.bot.reply_to(message, self.ctrl.get_top_user_metrics_in_this_chat(self.get_chatid()))

    def start_polling(self):
        return self.bot.infinity_polling()
