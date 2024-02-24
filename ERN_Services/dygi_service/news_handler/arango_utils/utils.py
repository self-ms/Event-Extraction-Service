from arango import client

class Arango:
    def __init__(self, collName):
        self.client = client.ArangoClient(hosts='http://hosts')
        self.collName=collName

        self.db = self.client.db('db', username='username', password='password')

        if self.db.has_collection(collName):
            self.coll = self.db.collection(collName)
        else:
            self.coll = self.db.create_collection(collName)
            self.coll.insert({'id':'test','doc':{'test':'test'}})

    def insert(self,doc):
        self.coll.insert(doc)
        # self.coll.insert_many({'name': 'jane', 'age': 19})

    def show(self,fild):
        cursor = self.db.aql.execute(f'FOR doc IN {self.collName} RETURN doc')
        doc_keys = [document['doc_key'] for document in cursor]
        print(doc_keys)

    def getDocIds(self,fild):
        cursor = self.db.aql.execute(f'FOR doc IN {self.collName} RETURN doc')
        doc_keys = [document[fild] for document in cursor]
        return doc_keys

    def checkDocExiste(self, docId):
        res = self.coll.find({"id":docId})
        return True if res.count() else False
