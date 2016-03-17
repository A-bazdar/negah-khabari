import sys
sys.path.append("/root/projects/negah-khabari")
sys.path.append("/root/projects/negah-khabari-user")

import datetime
import khayyam
from base_app.models.elasticsearch.news.news import NewsModel
from base_app.models.mongodb.bolton.bolton import BoltonModel
from base_app.models.mongodb.bolton_news.bolton_news import BoltonNewsModel
from base_app.models.mongodb.user.general_info.general_info import UserModel
from user_app.classes.access import PermissionClass

now = datetime.datetime.now()

def get_words(__dict, __key):
    try:
        return __dict[__key].split(',')
    except:
        return []


def get_searches(search, _start, _end):
    start = now.replace(hour=_start, minute=0, second=0, microsecond=0)
    end = now.replace(hour=_start + _end, minute=0, second=0, microsecond=0)
    all_words = search['all_words']
    try:
        key_words = search['key_words']
    except:
        key_words = []
    exactly_word = search['exactly_word']
    try:
        agency = search['agency']
        agency = [str(i['id']) for i in agency]
    except:
        agency = []
    each_words = search['each_words']
    without_words = search['without_words']

    return dict(all_words=all_words, exactly_word=exactly_word, each_words=each_words, without_words=without_words,
                start=start, end=end, agency=agency, key_words=key_words)

all_bolton = BoltonModel().get_all_automatic()['value']
for bolton in all_bolton:
    bolton_type = UserModel(_id=bolton['user']).get_bolton_type(bolton['type'])['value']
    for section in bolton['sections']:
        pattern_search = UserModel(_id=bolton['user']).get_pattern_search(section['pattern'])['value']
        _date = now.replace(hour=int(bolton_type['from']) + int(bolton_type['time_active']), minute=0, second=0, microsecond=0)
        if _date << now and (bolton['read_date'] is None or (now.date() != bolton['read_date'].date())):
            _search = get_searches(pattern_search['pattern_search'], int(bolton_type['from']), int(bolton_type['time_active']))
            permission = PermissionClass(user=bolton['user']).permission()
            full_current_user = dict(
                keyword=pattern_search['keyword']
            )
            for news in NewsModel(full_current_user=full_current_user, permission=permission).get_all_full(_search=_search)['value']:
                BoltonNewsModel(bolton=bolton['_id'], section=section['_id']).save(news=news)
            BoltonModel(_id=bolton['_id']).update_bolton_read_date(now)

