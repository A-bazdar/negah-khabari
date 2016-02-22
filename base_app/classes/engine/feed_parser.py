import feedparser


class FeedParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(url):
        try:
            url_parsed = feedparser.parse(url)
            if url_parsed is not False:
                return url_parsed.entries
            else:
                return []
        except:
            return []
