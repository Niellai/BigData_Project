import tweepy
import csv
import json
import os
import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
from kafka import KafkaProducer
from json import dumps


class LiveTweet(tweepy.StreamListener):
    def __init__(self, is_send_msg=True, api=None):
        super().__init__()
        self.stop_count = 30000
        self.count = 0
        self.is_send_msg = is_send_msg

        # Add your credentials here
        with open("TweetKeys.json", "r") as f:
            twitter_keys = json.load(f)

        auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
        auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])
        self.api = tweepy.API(auth)
        self.item_collection = []

        # initial Kafka producer
        self.send_topic = "transformed_tweet"
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

    def on_status(self, status):
        try:
            # if self.count >= self.stop_count:  # stop streaming
            #     return False

            json_str = json.dumps(status._json, indent=4, sort_keys=True)
            json_obj = json.loads(json_str)

            if json_obj.get('retweeted_status'):
                isRetweet = True
            else:
                isRetweet = False

            # Do we accept retweet or not
            item = []
            data = {}
            if not isRetweet:
                # Tweet information
                item.append(json_obj['id'])  # The integer representation of the unique identifier for this Tweet
                data['id'] = json_obj['id']

                item.append(json_obj['created_at'])  # UTC time when this Tweet was created.
                data['created_at'] = json_obj['created_at']

                item.append(json_obj['favorite_count'])
                data['favorite_count'] = json_obj['favorite_count']

                item.append(json_obj['retweet_count'])  # Number of times this Tweet has been retweeted.
                data['retweet_count'] = json_obj['retweet_count']

                sent = str(json_obj['text'])
                soup = BeautifulSoup(sent, 'lxml')
                item.append(soup.get_text())  # Actual text posted
                data['text'] = json_obj['text']

                # Nullable. Indicates approximately how many times this Tweet has been liked by Twitter users
                if json_obj.get('extended_tweet'):
                    sent = str(json_obj['extended_tweet']['full_text'])
                    soup = BeautifulSoup(sent, 'lxml')
                    item.append(soup.get_text())  # full text when over 280 chars limit
                    data['extended_tweet'] = json_obj['extended_tweet']['full_text']
                else:
                    item.append(None)

                item.append(json_obj['source'])  # Utility used to post the Tweet
                data['source'] = json_obj['source']

                # Nullable. Represents the geographic location of this Tweet as reported by the user or client application.
                item.append(json_obj['coordinates'])
                data['coordinates'] = json_obj['coordinates']

                # User information
                item.append(json_obj['user']['screen_name'])  # user who post this
                data['screen_name'] = json_obj['user']['screen_name']

                item.append(json_obj['user']['created_at'])  # user account creation date
                data['created_at'] = json_obj['user']['created_at']

                item.append(json_obj['user']['followers_count'])  # The number of followers this account currently has.
                data['followers_count'] = json_obj['user']['followers_count']

                item.append(json_obj['user']['verified'])  # When true, indicates that the user has a verified account.
                data['verified'] = json_obj['user']['verified']
                self.item_collection.append(item)
                # print('.', end="", flush=True)

                # if len(self.item_collection) > 100 and not self.send_msg:
                #     self.write_to_csv()
                #     self.print_records()

                if self.is_send_msg and len(data) > 0:
                    self.send_to_kafka(data)
        except Exception as e:
            print(str(e))
            # if len(self.item_collection) > 0 and not self.is_send_msg:
            #     self.write_to_csv()
            #     self.print_records()

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def write_to_csv(self):
        # date_str = datetime.now().strftime("%d-%m-%Y")  # per hr file
        date_str = datetime.now().strftime("%d-%m-%Y_%H00")  # per hr file
        file_name = 'tweets_{0}.csv'.format(date_str)
        if not os.path.exists(file_name):
            with open(file_name, 'a') as outfile:
                writer = csv.writer(outfile)
                cols = ['id', 'created_at', 'favorite_count', 'retweet_count', 'text', "extended_tweet",
                        'source', 'coordinates', 'screen_name', 'created_at', 'followers_count', 'verified']
                writer.writerow(cols)
        with open(file_name, 'a', encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            for i in self.item_collection:
                try:
                    writer.writerow(i)
                except Exception as e:
                    print("Write item error: ", str(e))
            self.item_collection = []

    def print_records(self):
        # date_str = datetime.now().strftime("%d-%m-%Y")  # per hr file
        date_str = datetime.now().strftime("%d-%m-%Y_%H00")  # per hr file
        file_name = 'tweets_{0}.csv'.format(date_str)
        df = pd.read_csv(file_name)
        print("total records: ", df.shape)

    def send_to_kafka(self, data):
        """
        Send extracted and transform tweet to Clean services

        :return: None
        """
        try:
            self.producer.send(self.send_topic, data)
        except Exception as e:
            print(str(e))


def main():
    track_terms = ['virus', 'covid2019', 'wuhan virus', 'coronavirus', 'outbreak',
                   'covid-19 death toll', 'covid-19', 'new COVID19', 'infected new case', 'pneumonia',
                   'recovered from covid-19', 'covid-19 patients discharged', 'symptoms', 'Singapore']
    languages = ['en']
    region = [103.585961, 1.153579, 104.103136, 1.483424]

    liveTweet = LiveTweet(is_send_msg=True)
    myStream = tweepy.Stream(auth=liveTweet.api.auth, listener=liveTweet)

    myStream.filter(track=track_terms, locations=region, languages=languages,
                    filter_level='low', is_async=True)
    print("Listening to live tweets...\n")

    # determine when to terminate
    # time.sleep(180) # in secs
    # myStream.disconnect()
    # liveTweet.write_to_csv()
    # liveTweet.print_records()


if __name__ == "__main__":
    print("Polling from RSS Feeds...\n")
    main()
