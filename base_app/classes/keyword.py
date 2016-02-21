from base_app.models.mongodb.keyword.keyword import KeyWordModel

__author__ = 'Morteza'


class KeyWordClass:
    def __init__(self, user_keyword=None):
        self.user_keyword = user_keyword

    def get_keyword_info(self, __key):
        user_keywords = self.user_keyword
        r = filter(lambda _key: _key['_id'] == __key, user_keywords)
        if len(r):
            return r[0]
        else:
            try:
                return KeyWordModel(_id=__key).get_one()["value"]
            except:
                pass
        return False

    def get_keywords(self, key_words):
        search_keywords = []
        for i in key_words:
            r = self.get_keyword_info(i)
            if r:
                search_keywords.append(r)

        key_query = ''
        for topic in search_keywords:
            _keyword = []
            _no_keyword = []
            for __key in topic['keyword']:
                _keyword += [__key['keyword']] + __key['synonyms']
                _no_keyword += __key['no_synonyms']

            keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _keyword).replace('AND  AND', 'AND')
            no_keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _no_keyword).replace('AND  AND', 'AND')
            _query = ''
            if keyword_query != '':
                _query += '({})'.format(keyword_query)

            if no_keyword_query != '':
                if _query == '':
                    _query += 'NOT({})'.format(no_keyword_query)
                else:
                    _query += ' AND NOT({})'.format(no_keyword_query)
            if key_query == '':
                key_query += '({})'.format(_query)
            else:
                key_query += ' OR ({})'.format(_query)

        return key_query

    def get_query_keyword(self):
        body = []
        user_keywords_ids = [i['_id'] for i in self.user_keyword]
        keywords = self.get_keywords(user_keywords_ids)

        if keywords != '':
            body.append({
                "query": {
                    "query_string": {
                        "fields": ["ro_title", "title", "summary", "body"],
                        "query": keywords
                    }
                }
            })
        return body

    def get_topics(self, key_words):
        search_keywords = []
        for i in key_words:
            r = self.get_keyword_info(i)
            if r:
                search_keywords.append(r)

        key_query = []
        for topic in search_keywords:
            _keyword = []
            _no_keyword = []
            for __key in topic['keyword']:
                _keyword += [__key['keyword']] + __key['synonyms']
                _no_keyword += __key['no_synonyms']

            keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _keyword).replace('AND  AND', 'AND')
            no_keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _no_keyword).replace('AND  AND', 'AND')
            _query = ''
            if keyword_query != '':
                _query += '({})'.format(keyword_query)

            if no_keyword_query != '':
                if _query == '':
                    _query += 'NOT({})'.format(no_keyword_query)
                else:
                    _query += ' AND NOT({})'.format(no_keyword_query)

            if _query != '':
                key_query.append(dict(query=_query, topic=topic['topic']))

        return key_query

    def get_list_query_topic(self):
        body = []
        user_keywords_ids = [i['_id'] for i in self.user_keyword]
        keywords = self.get_topics(user_keywords_ids)

        for query in keywords:
            body.append(dict(query={
                "query": {
                    "query_string": {
                        "fields": ["ro_title", "title", "summary", "body"],
                        "query": query['query']
                    }
                }
            }, topic=query['topic']))
        return body

    def get_list_keywords(self, key_words):
        search_keywords = []
        for i in key_words:
            r = self.get_keyword_info(i)
            if r:
                search_keywords.append(r)

        key_query = []
        for topic in search_keywords:
            for __key in topic['keyword']:
                _keyword = [__key['keyword']] + __key['synonyms']
                _no_keyword = __key['no_synonyms']

                keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _keyword).replace('AND  AND', 'AND')
                no_keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _no_keyword).replace('AND  AND', 'AND')
                _query = ''
                if keyword_query != '':
                    _query += '({})'.format(keyword_query)

                if no_keyword_query != '':
                    if _query == '':
                        _query += 'NOT({})'.format(no_keyword_query)
                    else:
                        _query += ' AND NOT({})'.format(no_keyword_query)

                if _query != '':
                    key_query.append(dict(query=_query, keyword=__key['keyword']))

        return key_query

    def get_list_query_keyword(self):
        body = []
        user_keywords_ids = [i['_id'] for i in self.user_keyword]
        keywords = self.get_list_keywords(user_keywords_ids)

        for query in keywords:
            body.append(dict(query={
                "query": {
                    "query_string": {
                        "fields": ["ro_title", "title", "summary", "body"],
                        "query": query['query']
                    }
                }
            }, keyword=query['keyword']))
        return body
