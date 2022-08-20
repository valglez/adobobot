# A class with all the controllers for the application
from datetime import datetime, timedelta

class BotControllers:
    def __init__(self, database):
        self.db = database

    def get_sort_metrics_by_chatid(self, chat_id, limit):
        return self.db.query_sort_metrics_by_chatid(chat_id, limit)

    def check_user(self, chat_id, user_id):
        return self.db.query_check_registred_users(chat_id, user_id)

    def get_ranking_metrics_in_this_chat(self, title, chat_id, user_id, limit):
        chat_title = title or 'este chat'
        if self.check_user(chat_id, user_id):
            response = 'TOP de mensajes en ' + chat_title + ':\n'
            for idx, id in enumerate(self.get_sort_metrics_by_chatid(chat_id, limit)):
                name = id['_id'] or 'Anonymous'
                idx += 1
                if idx == 1:
                    response += str(idx) + '. ' + name + ' (' + \
                        str(id['msgs']) + ') ' + str('🥇') + '\n'
                elif idx == 2:
                    response += str(idx) + '. ' + name + ' (' + \
                        str(id['msgs']) + ') ' + str('🥈') + '\n'
                else:
                    response += str(idx) + '. ' + name + ' (' + \
                        str(id['msgs']) + ') ' + str('🥉') + '\n'
            return response
        else:
            response = 'Sin registros.'
            return response

    def get_total_users_metrics_in_this_chat(self, chat_id, user_id, limit):
        if self.check_user(chat_id, user_id):
            response = ''
            for id in self.get_sort_metrics_by_chatid(chat_id, limit):
                name = id['_id'] or 'Anonymous'
                response += '• ' + name + ' ha escrito un total de ' + str(id['msgs']) + ' mensajes.\n'
            return response
        else:
            response = 'Sin registros.'
            return response

    def get_top_user_metrics_in_this_chat(self, chat_id, user_id, limit):
        if self.check_user(chat_id, user_id):
            response = ''
        for id in self.get_sort_metrics_by_chatid(chat_id, limit):
            name = id['_id'] or 'Anonymous'
            response += name + ' ha sido el usuario más activo con un total de ' + str(id['msgs']) + ' mensajes.'
            return response
        else:
            response = 'Sin registros.'
            return response

    def store_msg(self, user_id, date, chat_id, text):
        current_date = (datetime.fromtimestamp(date) -
                        timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        msg = {'userid': user_id,
               'date': current_date,
               'chatid': chat_id,
               'msgs': text}
        self.db.query_store_msg(msg)
       
    def upsert_user(self, user_id, name):
        query = {"userid":{"userid":user_id}}
        values = {"$set":{"name":name}}
        self.db.query_upsert_user(query,values)