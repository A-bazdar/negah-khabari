from config import Config
from elasticsearch import Elasticsearch
from web_app.classes.debug import Debug

__author__ = 'Morteza'
c = Config()


class ElasticSearchBaseModel():
    def __init__(self):
        self.db = Elasticsearch(host=c.web['elasticsearch']['host'], port=c.web['elasticsearch']['port'])


class ElasticSearchModel(ElasticSearchBaseModel):
    def __init__(self, _id=None, body=None, index=None, doc_type=None):
        ElasticSearchBaseModel.__init__(self)
        self.body = body
        self.index = index
        self.doc_type = doc_type
        self.id = _id

    def search(self):
        try:
            return self.db.search(index=self.index, doc_type=self.doc_type, body=self.body)

        except:
            Debug.get_exception()
            return False

    def insert(self):
        try:
            return self.db.index(index=self.index, doc_type=self.doc_type, id=self.id, body=self.body)
        except:
            return False

    def delete(self):
        try:
            self.db.delete(index=self.index, doc_type=self.doc_type, id=self.id)
            return True
        except:
            return False

    def update(self):
        try:
            self.db.update(index=self.index, doc_type=self.doc_type, id=self.id, body=self.body)
            return True
        except:
            return False

    def count_all(self):
        try:
            return self.db.count(index=self.index, doc_type=self.doc_type)['count']
        except:
            return 0

    def count(self):
        try:
            return self.db.count(index=self.index, doc_type=self.doc_type, body=self.body)['count']
        except:
            return 0

    def get_one(self):
        try:
            return self.db.get(index=self.index, doc_type=self.doc_type, id=self.id)
        except:
            return {}