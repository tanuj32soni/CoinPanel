import pymongo
import threading
import constants


class MongoClient:
    """
        This class is used to perform actions on the Mongo Database which the functions created.
        
        * insert_one() - This function is used to add one data dictionary into the database.
        * insert_in_background() - This function is used to save the data in background.
        * set_collection() - This function is used set the collection in the database when the
                           collection is already not created.
        * set_database() - This function is used set the database in the database when the
                        database is already not created.
    """
    def __init__(
        self,
        db_name,
        collection_name=None,
        host="localhost",
        port=27017,
        *args,
        **kwargs
    ):
        self._c = pymongo.MongoClient(host, port)

        self.set_database(db_name)
        if collection_name:
            self.set_collection(collection_name)

    def insert_one(self, data, collection_name):
        self.database[collection_name].insert_one(data)

    def insert_in_background(self, msg, collection_name):
        t = threading.Thread(target=self.insert_one, args=(msg, collection_name))
        t.start()

    def set_collection(self, collection_name):
        self.collection = self.database[collection_name]

    def set_database(self, db_name):
        self.database = self._c[db_name]


def initilize_database(db_user=None, db_password=None):
    """
        This function is used to initialize the MongoClient class object.
    """
    host = constants.HOST
    connect_host = constants.CONNECT_HOST
    port = int(constants.PORT)
    db_name = constants.DB_NAME
    collection_name = constants.COLLECTION_NAME
    try:
        if db_user and db_password:
            host = "mongodb://{}:{}@{}/{}".format(db_user, db_password, connect_host, db_name)
    except Exception as e:
        print("Error in database connection: ", str(e))
    db = MongoClient(db_name, host=host)

    return db
