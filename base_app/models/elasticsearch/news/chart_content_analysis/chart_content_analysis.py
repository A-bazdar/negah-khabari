#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from base_app.classes.date import CustomDateTime
from base_app.classes.debug import Debug
from base_app.models.elasticsearch.base_model import ElasticSearchModel
from base_app.models.mongodb.content.content import ContentModel

__author__ = 'Morteza'


class NewsChartContentAnalysisModel:
    index = 'negah_khabari'
    doc_type = 'news'

    def __init__(self):
        self.result = {'value': {}, 'status': False}
        self.end = datetime.datetime.now()
        self.start = CustomDateTime().generate_date_time(self.end, add=False, _type="months", value=1)
        self.value = []

    def get_count_content(self):
        try:
            __contents = ContentModel().get_all()['value']
            count_all = 0
            contents = []
            for con in __contents:
                body = {
                    "query": {
                        "filtered": {
                            "filter": {
                                "and": {
                                    "filters": [{
                                        "range": {
                                            "date": {
                                                "lt": self.end.isoformat(),
                                                "gte": self.start.isoformat()
                                            }
                                        }
                                    }, {
                                        "query": {
                                            "term": {
                                                "content": str(con['id'])
                                            }
                                        }
                                    }]
                                }
                            }
                        }
                    }
                }
                r = ElasticSearchModel(index=self.index, doc_type=self.doc_type, body=body).count()
                contents.append(dict(title=con['name'], value=r if r else 0))
                count_all += r if r else 0
            self.result['value'] = dict(contents=contents, count_all=count_all)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result
