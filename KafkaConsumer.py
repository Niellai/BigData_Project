import os
from datetime import datetime

import pandas as pd
from hdfs3 import HDFileSystem
from kafka import KafkaConsumer

"""
Reference:  https://arrow.apache.org/docs/python/csv.html
            https://arrow.apache.org/docs/python/parquet.html
            https://thegurus.tech/posts/2019/05/hadoop-python/
            https://wesmckinney.com/blog/python-hdfs-interfaces/

"""


class KafkaConsumer(object):

    def __init__(self, topics):
        # self.consumer = KafkaConsumer(
        #     topics,
        #     bootstrap_servers=['localhost:9092'],
        #     auto_offset_reset='earliest',
        #     enable_auto_commit=True,
        #     group_id='my-group',
        #     value_deserializer=lambda x: loads(x.decode('utf-8')))

        # self.HDFS = pa.HDFS.connect(host='localhost', port=9000)
        self.hdfs = HDFileSystem(host='localhost', port=9000)
        self.destination_path = ""
        self.dest_path_tweet = '/user/BigData/tweet_data'
        self.dest_path_rss = '/user/BigData/rss_data'
        self.dest_path_corona = '/user/BigData/corona_data'
        self.temp_path = 'temp_data'

    def write_to_file(self, source_df, data_type="tweet"):
        """
        Write collected data to HDFS.

        If file is collected on the same day, method will retrieve the previous dataframe
        combine it and write back to HDFS.

        Ref:    https://hdfs3.readthedocs.io/en/latest/

        :param source_df: Dataframe to be written
        :param data_type: "tweet", "rss", "corona" only these 3
        :return:
        """
        try:
            if len(source_df) > 0:
                if "tweet" in str(data_type).lower():
                    self.destination_path = self.dest_path_tweet
                elif "rss" in str(data_type).lower():
                    self.destination_path = self.dest_path_rss
                elif "corona" in str(data_type).lower():
                    self.destination_path = self.dest_path_corona
                else:
                    raise Exception("Invalid data type, unsure where to storage in HDFS.")

                # write to temp storage
                file_name = 'temp.csv'
                temp_path = os.path.join(self.temp_path, file_name)
                source_df.to_csv(temp_path)

                # check see if existing csv if yes combine them
                date_str = datetime.now().strftime("%d-%m-%Y")
                file_name = 'tweets_{0}.csv'.format(date_str)
                hdfs_path = os.path.join(self.destination_path, file_name)
                if self.hdfs.exists(hdfs_path):
                    with self.hdfs.open(hdfs_path) as f:
                        exist_df = pd.read_csv(f)
                        source_df = pd.concat([source_df, exist_df])
                        self.hdfs.rm(hdfs_path)  # remove and write a new one

                # pushing to HDFS
                self.hdfs.put(temp_path, hdfs_path)

                print("Write to HDFS completed: ", source_df.shape)
        except Exception as e:
            print(str(e))


def main():
    kc = KafkaConsumer('tweet')
    file = 'temp_data/tweets_small.csv'
    df = pd.read_csv(file)
    kc.write_to_file(df)


if __name__ == "__main__":
    main()
