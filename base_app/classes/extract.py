#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from base_app.classes.debug import Debug
from base_app.classes.timer import Timer
import dateutil.parser as d_parser

__author__ = 'Morteza'


class Extract:
    def __init__(self, base_link=None, link=None, ro_title=None, title=None, summary=None, thumbnail=None, body=None,
                 date=None, date_format=None, agency=None, sub_link=None, error_link=None, excludes=None, image=None):
        self.link = link
        self.ro_title = ro_title
        self.title = title
        self.base_link = base_link
        self.summary = summary
        self.thumbnail = thumbnail
        self.body = body
        self.excludes = excludes
        self.agency = agency
        self.date = date
        self.image = image
        self.date_format = date_format
        self.sub_link = sub_link
        self.error_link = error_link

    @staticmethod
    def get_date_str(_date):
        a = ''
        for i in u'{}'.format(_date):
            try:
                a += u'{}'.format(str(int(i)))
            except:
                a += u'{}'.format(i)
        return a

    def get_link(self, __soap, __link):
        try:
            if __link is not False:
                link = __soap.select_one(__link).find('a')['href'].encode('utf-8')
            else:
                link = __soap.find('a')['href'].encode('utf-8')
            if 'http' not in link and 'www' not in link:
                link = self.base_link.encode('utf-8') + link
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_link',
                                data=self.error_link)
            link = None
        return link

    def get_ro_title(self, __soap, __ro_title):
        try:
            if __ro_title is not False:
                ro_title = __soap.select_one(__ro_title).text.encode('utf-8').strip()
            else:
                ro_title = None
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_ro_title',
                                data=self.error_link)
            ro_title = None
        return ro_title

    def get_title(self, __soap, __title):
        try:
            title = __soap.select_one(__title).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_title',
                                data=self.error_link)
            title = None
        return title

    def get_summary(self, __soap, __summary):
        try:
            if __summary is not False:
                summary = __soap.select_one(__summary).text.encode('utf-8').strip()
            else:
                summary = None
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_summary',
                                data=self.error_link)
            summary = None
        return summary

    def get_image(self, __soap, __image):
        try:
            if __image is not False:
                image = __soap.select_one(__image).find('img')['src'].encode('utf-8')
            else:
                image = None
            if image is not None and 'http' not in image and 'www' not in image:
                image = self.base_link.encode('utf-8') + image
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_image',
                                data=self.error_link)
            image = None
        return image

    def get_thumbnail(self, __soap, __thumbnail):
        try:
            try:
                if __thumbnail is not False:
                    thumbnail = __soap.select_one(__thumbnail).find('img')['src'].encode('utf-8')
                else:
                    thumbnail = __soap.find('img')['src'].encode('utf-8')
            except:
                thumbnail = __soap.select_one(__thumbnail)['src'].encode('utf-8')
            if thumbnail is not None and 'http' not in thumbnail and 'www' not in thumbnail:
                thumbnail = self.base_link.encode('utf-8') + thumbnail
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_thumbnail',
                                data=self.error_link)
            thumbnail = None
        return thumbnail

    def get_body(self, __soap, __body, __excludes):
        try:
            body = None
            if __body is not None:
                body_tag = __soap.select_one(__body)
                body = __soap.select_one(__body).encode('utf-8').strip()
                for i in __excludes:
                    ex = body_tag.select_one(i).encode('utf-8').strip()
                    body = body.replace(ex, '')
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_body_news', data=self.error_link)
            body = None
        return body

    def get_images(self, __soap, __body, __excludes, __image):
        try:
            img = []
            if __body is not None:
                images = __soap.select_one(__body).find_all('img')
                body_tag = __soap.select_one(__body)
                images_ex = []
                for i in __excludes:
                    images_ex += body_tag.select_one(i).find_all('img')
                images_ex = [i['src'] for i in images_ex]
                for i in images:
                    if i['src'] not in images_ex:
                        __img = i['src'].encode('utf-8').strip()
                        if 'http' not in __img and 'www' not in __img:
                            __img = self.base_link.encode('utf-8') + __img
                        if __img != __image:
                            img.append(__img)
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_body_news', data=self.error_link)
            img = []
        return img

    def get_video(self, __soap, __body):
        try:
            video = None
            if __body is not None:
                try:
                    video = __soap.select_one(__body).find('video')['src'].encode('utf-8').strip()
                except:
                    video = __soap.select_one(__body).find('embed')['src'].encode('utf-8').strip()
                if 'http' not in video and 'www' not in video:
                    video = self.base_link.encode('utf-8') + video
                video = video if not any(sub in video.lower() for sub in ["mp3", "wav", "wma", "ogg"]) else None
        except:
            video = None
        return video

    def get_sound(self, __soap, __body):
        try:
            sound = None
            if __body is not None:
                sound = __soap.select_one(__body).find('embed')['src'].encode('utf-8').strip()
                if 'http' not in sound and 'www' not in sound:
                    sound = self.base_link.encode('utf-8') + sound
                sound = sound if any(substring in sound.lower() for substring in ["mp3", "wav", "wma", "ogg"]) else None
        except:
            sound = None
        return sound

    def get_date(self, __soap, __date, __date_format):
        try:
            news_date = __soap.select_one(__date).text.replace(u'ي', u'ی').strip()
            news_date.encode('utf-8')
            news_date = self.get_date_str(news_date)
            return khayyam.JalaliDatetime().strptime(news_date, u'{}'.format(__date_format)).todatetime()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_date_news', data=self.error_link)
            return datetime.datetime.now()

    def get_news_info(self, list_news, link, title, summary, thumbnail):
        news = []
        for i in list_news:
            self.error_link = None
            t = Timer()
            __link = self.get_link(i, link)
            __link_time = t.end()
            t.start()
            __title = self.get_title(i, title)
            __title_time = t.end()
            t.start()
            __summary = self.get_summary(i, summary)
            __summary_time = t.end()
            t.start()
            __thumbnail = self.get_thumbnail(i, thumbnail)
            __thumbnail_time = t.end()
            if __link is not None and __title is not None:
                news.append(dict(
                    news=dict(link=__link, title=__title, summary=__summary, thumbnail=__thumbnail),
                    time=dict(link=__link_time, title=__title_time, summary=__summary_time, thumbnail=__thumbnail_time),
                ))
        return news

    def get_news(self, __doc, __type, __selectors):
        t = Timer()
        ro_title = self.get_ro_title(__doc, __selectors['ro_title'])
        ro_title_time = t.end()
        t.start()
        image = self.get_image(__doc, __selectors['image'])
        image_time = t.end()
        t.start()
        body = self.get_body(__doc, __selectors['body'], __selectors['excludes'])
        body_time = t.end()
        t.start()
        images = self.get_images(__doc, __selectors['body'], __selectors['excludes'], image)
        images_time = t.end()
        t.start()
        video = self.get_video(__doc, __selectors['body'])
        video_time = t.end()
        t.start()
        sound = self.get_sound(__doc, __selectors['body'])
        sound_time = t.end()
        t.start()
        if __type != "RSS":
            date = self.get_date(__doc, __selectors['date'], __selectors['date_format'])
        else:
            date = None
        date_time = t.end()
        ret = dict(
            ro_title=ro_title,
            image=image,
            body=body,
            video=video,
            date=date,
            sound=sound,
            images=images,
        )
        ret_time = dict(
            ro_title=ro_title_time,
            image=image_time,
            body=body_time,
            video=video_time,
            date=date_time,
            sound=sound_time,
            images=images_time,
        )
        return ret, ret_time

    def get_rss(self, doc, summary):
        t_2 = Timer()
        ro_title = self.get_ro_title(doc, self.ro_title)
        ro_title_time = t_2.end()
        t_2 = Timer()
        title = self.title
        title_time = t_2.end()
        t_2 = Timer()
        if summary is None or summary == '':
            summary = self.get_summary(doc, self.summary)
        summary_time = t_2.end()
        t_2 = Timer()
        image = self.get_image(doc, self.image)
        thumbnail_time = t_2.end()
        t_2 = Timer()
        body = self.get_body(doc, self.body, self.excludes)
        body_time = t_2.end()
        t_2 = Timer()
        images = self.get_images(doc, self.body, self.excludes, self.image)
        images_time = t_2.end()
        t_2 = Timer()
        video = self.get_video(doc, self.body)
        video_time = t_2.end()
        t_2 = Timer()
        sound = self.get_sound(doc, self.body)
        sound_time = t_2.end()
        t_2 = Timer()
        try:
            date = d_parser.parse(self.date)
        except:
            date = datetime.datetime.now()
        date_time = t_2.end()
        return dict(
            news=dict(
                ro_title=ro_title,
                title=title,
                summary=summary,
                image=image,
                body=body,
                date=date,
                video=video,
                sound=sound,
                images=images,
            ),
            time=dict(
                ro_title=ro_title_time,
                title=title_time,
                summary=summary_time,
                thumbnail=thumbnail_time,
                body=body_time,
                images=images_time,
                video=video_time,
                sound=sound_time,
                date=date_time,
            )
        )
