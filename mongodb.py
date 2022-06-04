import pymongo
import pandas as pd

class db_ops:
    def __init__(self, db, coll):
        self.db = db
        self.coll = coll


    def load_df(self):

        client = pymongo.MongoClient("mongodb+srv://mongodb:mongodb@cluster0.grv2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client[self.db]
        coll = self.coll
        error_msg=''

        if self.db in client.list_database_names():
            if self.coll in db.list_collection_names():
                pass
            else:
                error_msg = self.coll + ' collection is not available in mongoDb'

        else:
            error_msg=self.db + ' database is not available in mongoDb'


        if error_msg =='':
            data = pd.DataFrame(list(db.Test.find()))
            data = data.iloc[:, 1:]
            return data
        else:
            return error_msg