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


def get_words(__dict, __key):
    try:
        return __dict[__key].split(',')
    except:
        return []


def get_period(__dict):
    try:
        now = datetime.datetime.today()
        start = None
        end = None
        if __dict['period'] == 'hour':
            start = now - datetime.timedelta(hours=1)
            end = now
        elif __dict['period'] == 'half-day':
            start = now - datetime.timedelta(hours=12)
            end = now
        elif __dict['period'] == 'day':
            start = now - datetime.timedelta(days=1)
            end = now
        elif __dict['period'] == 'week':
            start = now - datetime.timedelta(weeks=1)
            end = now
        elif __dict['period'] == 'month':
            start = now - datetime.timedelta(days=30)
            end = now
        elif __dict['period'] == 'period':
            start = khayyam.JalaliDatetime().strptime(__dict['start_date'] + ' 00:00:00', "%Y/%m/%d %H:%M:%S").todatetime()
            end = khayyam.JalaliDatetime().strptime(__dict['end_date'] + ' 23:59:59', "%Y/%m/%d %H:%M:%S").todatetime()
        return start, end
    except:
        return None, None


def get_searches(search):
    start, end = get_period(search)
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
now = datetime.datetime.now()
all_bolton = BoltonModel().get_all_automatic()['value']
for bolton in all_bolton:
    bolton_type = UserModel(_id=bolton['user']).get_bolton_type(bolton['type'])['value']
    for section in bolton['sections']:
        pattern_search = UserModel(_id=bolton['user']).get_pattern_search(section['pattern'])['value']
        # if (int(bolton_type['from']) <= now.hour <= int(bolton_type['from']) + int(bolton_type['time_active'])) and (bolton_type['read_date'] is None or (now - bolton_type['read_date']).days < 1):
        _search = get_searches(pattern_search['pattern_search'])
        permission = PermissionClass(user=bolton['user']).permission()
        full_current_user = dict(
            keyword=pattern_search['keyword']
        )
        for news in NewsModel(full_current_user=full_current_user, permission=permission).get_all_full(_search=_search)['value']:
            print bolton['_id'], type(bolton['_id'])
            print section['_id'], type(section['_id'])
                # BoltonNewsModel(bolton=bolton['_id'], section=section['_id']).save(news=news)

