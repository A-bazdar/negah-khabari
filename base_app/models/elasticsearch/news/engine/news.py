import time
import datetime

from base_app.classes.public import Hash, CreateId
from base_app.models.elasticsearch.base_model import ElasticSearchModel
from base_app.models.mongodb.base_model import MongodbModel


class News:
    doc_type = 'news'
    result = {'value': {}, 'status': False}

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, image=None,
                 agency=None, subject=None, body=None, date=None, content=None, images=None, video=None,
                 sound=None, geographic=None, group=None, category=None, direction=None):
        if images is None:
            images = []
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.body = body
        self.subject = subject
        self.category = category
        self.date = date
        self.image = image
        self.thumbnail = thumbnail
        self.link = link
        self.content = content
        self.images = images
        self.video = video
        self.sound = sound
        self.geographic = geographic
        self.group = group
        self.direction = direction

    def is_exist(self):
        try:
            if self.title is not None:
                body = {
                    "query": {
                        "filtered": {
                            "filter": {
                                "or": {
                                    "filters": [
                                        {
                                            "and": {
                                                "filters": [
                                                    {
                                                        "query": {
                                                            "term": {
                                                                "hash_title": Hash.hash(self.title)
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "query": {
                                                            "term": {
                                                                "agency": self.agency,
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "query": {
                                                "term": {
                                                    "hash_link": Hash.hash(self.link)
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            else:
                body = {
                    "query": {
                        "term": {
                            "hash_link": Hash.hash(self.link)
                        }
                    }
                }
            x = ElasticSearchModel(doc_type=self.doc_type, body=body).count()
            if x:
                return True
            return False
        except:
            return False

    @staticmethod
    def insert_mongodb(body):
        MongodbModel(body=body, collection='news').insert()
        if MongodbModel(body={}, collection='news').count() > 60:
            n = MongodbModel(body={}, collection='news', sort="date", page=1, size=1, ascending=1).get_all_pagination()
            _id = 0
            for i in n:
                _id = i['_id']
            MongodbModel(body={"_id": _id}, collection='news').delete()

    def insert(self):
        d = datetime.datetime.now()
        body = {
            'link': self.link,
            'hash_link': Hash.hash(self.link),
            'title': self.title,
            'hash_title': Hash.hash(self.title),
            'ro_title': self.ro_title,
            'summary': self.summary,
            'body': self.body,
            'thumbnail': self.thumbnail,
            'agency': self.agency,
            'subject': self.subject,
            'category': self.category,
            'direction': self.direction,
            'date': self.date,
            'content': self.content,
            'image': self.image,
            'images': self.images,
            'video': self.video,
            'sound': self.sound,
            'geographic': self.geographic,
            'group': self.group,
            'read_date': d,
            'read_timestamp': int(time.mktime(d.timetuple())),
        }
        news = CreateId().create_object_id()
        self.result['value'] = ElasticSearchModel(doc_type=self.doc_type, body=body,
                                                  _id=news).insert()
        self.insert_mongodb(body)
        self.result['status'] = True
        return self.result

    def update(self):
        body = {
            "script": "ctx._source.ro_title = __ro_title;ctx._source.image = __image;"
                      "ctx._source.body = __body;ctx._source.video = __video;"
                      "ctx._source.sound = __sound;ctx._source.images = __images",
            "params": {
                "__ro_title": self.ro_title,
                "__image": self.image,
                "__body": self.body,
                "__video": self.video,
                "__sound": self.sound,
                "__images": self.images,
            }
        }
        if self.date is not None:
            body['script'] += ";ctx._source.date = __date"
            body['params']['__date'] = self.date
        self.result['value'] = ElasticSearchModel(doc_type=self.doc_type, body=body,
                                                  _id=self.id).update()
        self.result['status'] = True
        return self.result

    def insert_queue(self, _type=None, _news=None, _base_link=None, _title=None, _selectors=None):
        body = dict(
            news=_news,
            code=-1,
            link=self.link,
            agency=self.agency,
            type=_type,
            date=self.date,
            base_link=_base_link,
            title=_title,
            **_selectors
        )
        if _type == "COMPARATIVE":
            __collection = 'news_comparative_queue'
        else:
            __collection = 'news_queue'
        self.result['value'] = str(MongodbModel(collection=__collection, body=body).insert())
        self.result['status'] = True

    @staticmethod
    def delete_queue(_type=None, _code=None):
        body = {
            "code": _code,
        }
        if _type == "COMPARATIVE":
            __collection = 'news_comparative_queue'
        else:
            __collection = 'news_queue'
        MongodbModel(collection=__collection, body=body).delete()
