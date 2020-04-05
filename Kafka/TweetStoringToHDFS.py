import os
from datetime import datetime
from json import loads
import pandas as pd
import json

from kafka import KafkaConsumer

from BigData_Project.HDFS.HDFSUtil import HDFSUtil


class TweetStoringToHDFS(object):

    def __init__(self):
        super().__init__()

        self.listen_topic = "sentiment_tweet"

        self.is_listening = True
        self.consumer = KafkaConsumer(
            self.listen_topic,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        self.send_topic = "new_tweet"
        self.hdfsUtil = HDFSUtil()
        self.curFile = ""
        self.df = None
        self.save_at_batches = 1000  # control how frequent we save our file

    def write_tweet(self):
        while self.is_listening:
            for message in self.consumer:
                # get current datetime as file name
                date_str = datetime.now().strftime("%d-%m-%Y")
                file_name = 'tweets_{0}.csv'.format(date_str)

                if self.curFile == "" or self.curFile != file_name:
                    # Load current HDFS file as df
                    if self.hdfsUtil.is_file_exist(file_name):
                        self.df = self.hdfsUtil.read_file_dataframe(file_name)
                        self.curFile = file_name
                    else:
                        # TODO: Write to HDFS before creating new one, if contain data
                        # HDFS file does not exist, create empty data frame
                        self.curFile = file_name
                        self.df = pd.DataFrame()

                # Read json object and load it into data frame
                json_object = dict(message.value)
                cur_df = pd.DataFrame(list(json_object.values())).T
                cur_df.columns = list(json_object.keys())

                # Append the new tweet
                frames = [self.df, cur_df]
                self.df = pd.concat(frames)

                # saving the result at 1000 new tweets
                if len(self.df) % self.save_at_batches == self.save_at_batches:
                    temp_path = os.path.join("../HDFS", self.hdfsUtil.temp_types["tweet"])
                    self.df.to_csv(temp_path, index=False)
                    self.hdfsUtil.write_file(temp_path, file_name)


if __name__ == "__main__":
    print("Listening to write tweets to HDFS...\n")
    tweetToHDFS = TweetStoringToHDFS()
    tweetToHDFS.write_tweet()
