
import pymongo


class Database:
    def __init__(self, conn, db_name, db_col):
        self.connection = pymongo.MongoClient(conn)
        self.db = self.connection[db_name]
        self.collection = self.db[db_col]

    def connect(self):
        return self.collection

    def query_count_chats_for_user(self, chat_id, user_id):
        return self.collection.count_documents({'chatid': chat_id, 'userid': user_id})

    def query_get_user_by_id(self, chat_id, user_id):
        return self.collection.find({'chatid': chat_id, 'userid': user_id})

    def query_get_total_users_metrics(self, chat_id):
        return self.collection.distinct('userid', {'chatid': chat_id})

    def query_sort_metrics_by_chatid(self, chat_id, limit):
        pipeline = (
            {'$match': {'chatid': chat_id}},
            {'$group': {'_id': '$name', 'msgs': {'$sum': 1}}},
            {'$sort': {'msgs': -1}},
            {'$limit': limit})
        return self.collection.aggregate(list(pipeline))

    def query_store_msg(self, object):
        self.collection.insert_one(object)
