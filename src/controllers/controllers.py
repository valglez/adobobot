# A class with all the controllers for the application
from datetime import datetime, timedelta


class BotControllers:
    def __init__(self, database):
        self.db = database

    def count_chats_for_user(self, chat_id, user_id):
        return self.db.query_count_chats_for_user(chat_id, user_id)

    def get_user_by_id(self, chat_id, user_id):
        result = self.db.query_get_user_by_id(chat_id, user_id)
        return result[0]['name'] or 'Anonymous'

    def get_total_users_metrics(self, chat_id):
        return self.db.query_get_total_users_metrics(chat_id)

    def get_sort_metrics_by_chatid(self, chat_id, limit):
        return self.db.query_get_sort_metrics_by_chatid(chat_id, limit or 2)

    def get_top_user_metrics_by_chatid(self, chat_id):
        return self.db.query_get_sort_metrics_by_chatid(chat_id, 1)

    def get_total_users_metrics_by_chat(self, chat_id):
        mylist = []
        users_id = self.get_total_users_metrics(chat_id)
        for id in users_id:
            username = self.get_user_by_id(chat_id, id)
            user_chats = self.count_chats_for_user(chat_id, id)
            mydict = {}
            mydict['name'] = username
            mydict['msgs'] = user_chats
            mylist.append(mydict)
        return mylist

    def get_ranking_metrics_in_this_chat(self, title, chat_id, limit):
        chat_title = title or 'este chat'
        if self.get_total_users_metrics_by_chat(chat_id):
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

    def get_total_users_metrics_in_this_chat(self, chat_id, limit):
        if self.get_total_users_metrics_by_chat(chat_id):
            response = ''
            for id in self.get_sort_metrics_by_chatid(chat_id, limit):
                name = id['_id'] or 'Anonymous'
                response += 'El usuario ' + name + ' ha escrito un total de ' + \
                    str(id['msgs']) + ' mensajes.\n'
            return response
        else:
            response = 'Sin registros.'
            return response

    def get_top_user_metrics_in_this_chat(self, chat_id):
        if self.get_total_users_metrics_by_chat(chat_id):
            response = ''
            for id in self.get_top_user_metrics_by_chatid(chat_id):
                name = id['_id'] or 'Anonymous'
                response += 'El usuario ' + name + \
                    ' ha sido el usuario más activo con un total de ' + \
                    str(id['msgs']) + ' mensajes.'
            return response
        else:
            response = 'Sin registros.'
            return response

    def store_msg(self, user_id, username, date, chat_id, text):
        current_date = (datetime.fromtimestamp(date) -
                        timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        msg = {'userid': user_id,
               'name': username,
               'date': current_date,
               'chatid': chat_id,
               'msgs': text}
        self.db.query_store_msg(msg)
