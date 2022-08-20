import pymongo

class Database:
    def __init__(self, conn, db_name, db_col):
        self.connection = pymongo.MongoClient(conn)
        self.db = self.connection[db_name]
        self.collection = self.db[db_col]

    def query_check_registred_users(self, chat_id, user_id):
        return self.collection.count_documents({'chatid': chat_id, 'userid': user_id})

    def query_sort_metrics_by_chatid(self, chat_id, limit):
        pipeline = (
            {'$match': {'chatid': chat_id}},
            {'$group': {'_id': '$name', 'msgs': {'$sum': 1}}},
            {'$sort': {'msgs': -1}},
            {'$limit': limit})
        return self.collection.aggregate(list(pipeline))

    def query_store_msg(self, object):
        self.collection.insert_one(object)

    # TO DO 
    #
    #def query_store_user(self, object):
    #    self.collection.insert_one(object)