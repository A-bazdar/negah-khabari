import feedparser

from base_app.classes.timer import Timer


class FeedParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(url):
        try:
            t = Timer()
            url_parsed = feedparser.parse(url)
            if url_parsed is not False:
                return url_parsed.entries, t.end()
            else:
                return [], t.end()
        except:
            return [], 0
