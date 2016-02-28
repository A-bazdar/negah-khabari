from bson import ObjectId


class FeedStatisticTimesSaveNews:
    def __init__(self):
        self.body = 0
        self.ro_title = 0
        self.date = 0
        self.video = 0
        self.images = 0
        self.sound = 0
        self.title = 0
        self.summary = 0
        self.thumbnail = 0
        self.extract_news = 0
        self.extract = 0
        self.save = 0
        self.read_news_url = 0
        self.time = 0
        self.link = ""
        self._id = ObjectId()
        self.is_exist = 0

    def set_times(self, times):
        self.title = times['title']
        self.summary = times['summary']
        self.thumbnail = times['thumbnail']


class FeedStatisticTimes:
    def __init__(self):
        self._id = ObjectId()
        self.link = ""
        self.extract_news_links = 0
        self.read_news_links = 0
        self.time = 0
        self.save_news = []

    def add_save_news(self, save_news):
        self.save_news.append(save_news.__dict__)


class FeedStatistic:
    def __init__(self):
        self.count_all_links = 0
        self.count_links_read_with_news = 0
        self.count_read_news = 0
        self.count_last_read_news = 0
        self.times = []

    def inc_count_all_links(self):
        self.count_all_links += 1

    def inc_count_links_read_with_news(self):
        self.count_links_read_with_news += 1

    def inc_count_read_news(self):
        self.count_read_news += 1

    def inc_count_last_read_news(self):
        self.count_last_read_news += 1

    def add_times(self, times):
        self.times.append(times.__dict__)
