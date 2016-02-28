from base_app.models.redis.model.model import RedisModel


class FeedStatisticRedis:
    def __init__(self):
        pass

    @staticmethod
    def last_read_links(value):
        if value is not None:
            RedisModel('last_read_links', value).set()
        else:
            return RedisModel('last_read_links').get()

    @staticmethod
    def count_all_links(value):
        if value is not None:
            RedisModel('count_all_links', value).set()
        else:
            return RedisModel('count_all_links').get()

    @staticmethod
    def last_read_news(value):
        if value is not None:
            RedisModel('last_read_news', value).set()
        else:
            return RedisModel('last_read_news').get()

    @staticmethod
    def count_last_read_news(value):
        if value is not None:
            RedisModel('count_last_read_news', value).set()
        else:
            return RedisModel('count_last_read_news').get()

    @staticmethod
    def feed_statistic_id(value):
        if value is not None:
            RedisModel('feed_statistic_id', value).set()
        else:
            return RedisModel('feed_statistic_id').get()

    @staticmethod
    def count_links_read_with_news(value):
        if value is not None:
            RedisModel('count_links_read_with_news', value).set()
        else:
            return RedisModel('count_links_read_with_news').get()

    @staticmethod
    def count_read_news(value):
        if value is not None:
            RedisModel('count_read_news', value).set()
        else:
            return RedisModel('count_read_news').get()
