from json import dumps

import feedparser
import time

from kafka import KafkaProducer


class RSSLive(object):
    def __init__(self):
        super().__init__()
        self.is_listening = True
        self.is_send_msg = True
        self.last_etag = None
        self.last_modified = None
        self.rss_list = []
        self.news_urls = {
            'straitstimes_asia': 'https://www.straitstimes.com/news/asia/rss.xml',
            'straitstimes_sg': "https://www.straitstimes.com/news/singapore/rss.xml",
            'cna_asia': "https://www.channelnewsasia.com/rssfeeds/8395744",
            'cna_singapore': "https://www.channelnewsasia.com/rssfeeds/8396082",
            'sg': 'https://rss.app/feeds/xU6SJpiMAfTWwJ73.xml',
            'wuhan': 'https://rss.app/feeds/Tl969wE8IeWxNSB9.xml',
            'covid19': 'https://rss.app/feeds/i4YNqlh35xUILXSn.xml',
            'corona': 'https://rss.app/feeds/Om145yWzbSEt8OTt.xml',
        }

        # initial Kafka producer
        self.send_topic = "transformed_rss"
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

    def get_news(self, rss_url):
        """
        Function grabs the rss feed headlines (titles) and returns them as a list.

        :return:
        """
        feed = feedparser.parse(rss_url)
        # Check if etag is repeated
        if feed.status == 200:
            for item in feed['items']:
                try:
                    if not self.is_repeated(item['title']):
                        rss_item = {'title': item['title'], 'link': item['link'], 'published': item['published']}
                        self.rss_list.append(rss_item)
                except Exception as e:
                    print(str(e))

            if len(self.rss_list) > 0 and self.is_send_msg:
                self.send_to_kafka(self.rss_list)

    def is_repeated(self, title):
        for rss in self.rss_list:
            if title in rss['title']:
                return True
        return False

    def listen_rss(self):
        while self.is_listening:
            try:
                for key, url in self.news_urls.items():
                    self.get_news(url)
                time.sleep(60 * 1)  # 1 min * 5
            except Exception as e:
                print(str(e))

    def send_to_kafka(self, data):
        """
        Send extracted and transform RSS to Clean services

        :return: None
        """
        try:
            self.producer.send(self.send_topic, data)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    print("Polling from RSS Feeds...")
    rssLive = RSSLive()
    rssLive.listen_rss()
