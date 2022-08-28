import pymongo

class Database:
    def __init__(self, conn, db_name, db_col):
        self.connection = pymongo.MongoClient(conn)
        self.db = self.connection[db_name]
        self.col_logs = self.db[db_col[1:4]]
        self.col_users = self.db[db_col[5:10]]
        
    def query_check_user_docs_by_chatid(self, chat_id, user_id):
        return self.col_logs.count_documents({'chatid': chat_id, 'userid': user_id})

    def query_get_username(self):
        return self.col_users.find()
    
    def query_get_username_by_userid(self, user_id):
        return self.col_users.find({'userid': user_id})

    def query_sort_metrics_by_chatid(self, chat_id, limit):
        pipeline = (
            {'$match': {'chatid': chat_id}},
            {'$group': {'_id': '$userid', 'msgs': {'$sum': 1}}},
            {'$sort': {'msgs': -1}},
            {'$limit': limit},
            {'$project': {'_id': 0,'msgs': 1,'userid': '$_id'}})
        return self.col_logs.aggregate(list(pipeline))

    def query_store_msg(self, object):
        self.col_logs.insert_one(object)

    def query_upsert_user(self, query, values):
        self.col_users.update_many(query, values, upsert=True)