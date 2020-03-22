import os
from os import listdir
from os.path import isfile, join

from hdfs3 import HDFileSystem
import pandas as pd


class HDFSUtil(object):
    """
    Reference: https://hdfs3.readthedocs.io/en/latest/api.html

    HDFS utility handles read, write, delete files
    """

    def __init__(self):
        self.hdfs = HDFileSystem(host='localhost', port=9000)
        self.dest_path_tweet = '/user/BigData/tweet_data'
        self.dest_path_rss = '/user/BigData/rss_data'
        self.dest_path_corona = '/user/BigData/corona_data'
        self.destination_path = ""
        self.import_path = '../import_data'
        self.import_path_tweet = os.path.join(self.import_path, 'tweets')
        self.import_path_rss = os.path.join(self.import_path, 'rss')
        self.import_path_corona = os.path.join(self.import_path, 'corona')

        self.hdfs_types = {'tweet': self.dest_path_tweet, 'rss': self.dest_path_rss, 'corona': self.dest_path_corona}
        self.import_types = {'tweet': self.import_path_tweet, 'rss': self.import_path_rss,
                             'corona': self.import_path_corona}
        self.temp_types = {'tweet': "TempData/temp_tweet.csv", "rss": "TempData/temp_rss.csv",
                           "corona": "TempData/temp_corona.csv"}

    def get_files(self, data_type):
        """
        Return a list of files contain inside HDFS.

        :param data_type: in string only accept 'tweet', 'rss', 'corona'

        :return: list of files stored in HDFS
        """
        if "tweet" == str(data_type).lower():
            self.destination_path = self.dest_path_tweet
        elif "rss" == str(data_type).lower():
            self.destination_path = self.dest_path_rss
        elif "corona" == str(data_type).lower():
            self.destination_path = self.dest_path_corona
        else:
            raise Exception("Invalid data type, check if input string is correct.")

        if self.hdfs.exists(self.destination_path):
            return self.hdfs.ls(self.destination_path)

    def import_local_data(self, overwrite=False):
        """
        Import files from local storage folder "import_data".

        Will print out files that is being push to HDFS.

        :return: None
        """
        for data_type in self.import_types.keys():
            try:
                hdfs_files = self.get_files(data_type)
                local_folder = self.import_types[data_type]
                onlyfiles = [f for f in listdir(local_folder) if isfile(join(local_folder, f) and ".~" not in f)]

                for file in onlyfiles:
                    try:
                        if overwrite:
                            dest_path = self.hdfs_types[data_type]
                            self.hdfs.put(os.path.join(local_folder, file), os.path.join(dest_path, file))
                            print(f"Write to HDFS: {os.path.join(dest_path, file)}")
                        else:
                            if sum([file in f for f in hdfs_files]) == 0 or len(hdfs_files) == 0:
                                dest_path = self.hdfs_types[data_type]
                                self.hdfs.put(os.path.join(local_folder, file), os.path.join(dest_path, file))
                                print(f"Write to HDFS: {os.path.join(dest_path, file)}")
                    except Exception as e:
                        print(str(e))

            except Exception as e:
                print(str(e))

    def delete_file(self, file_name, data_type=None):
        """
        Attempt to delete file in HDFS by file name.

        :param file_name: Case sensitive
        :param data_type: Which data type to delete from 'tweet', 'rss', 'corona'
        :return: True if successful else False
        """
        try:
            del_count = 0
            for mdata_type in self.hdfs_types.keys():
                if data_type:
                    if mdata_type == data_type:
                        hdfs_path = self.hdfs_types[mdata_type]
                        hdfs_path = os.path.join(hdfs_path, file_name)
                        if self.hdfs.exists(hdfs_path):
                            self.hdfs.rm(hdfs_path)
                            print(f"File deleted: {file_name}")
                            del_count += 1
                else:
                    hdfs_path = self.hdfs_types[mdata_type]
                    hdfs_path = os.path.join(hdfs_path, file_name)
                    if self.hdfs.exists(hdfs_path):
                        self.hdfs.rm(hdfs_path)
                        print(f"File deleted: {file_name}")
                        del_count += 1

            if del_count == 0:
                print(f"Could not find file in HDFS: {file_name}")
                return False
            else:
                return True
        except Exception as e:
            print(str(e))
            return False

    def is_file_exist(self, file_name):
        try:
            for data_type in self.hdfs_types.keys():
                hdfs_path = self.hdfs_types[data_type]
                hdfs_path = os.path.join(hdfs_path, file_name)
                if self.hdfs.exists(hdfs_path):
                    return True
            return False
        except Exception as e:
            print(str(e))

    def read_file(self, file_name):
        """
        Return the DataFrame load from HDFS

        :param file_name: Case sensitive
        :return: DataFrame
        """
        try:
            for data_type in self.hdfs_types.keys():
                hdfs_path = self.hdfs_types[data_type]
                hdfs_path = os.path.join(hdfs_path, file_name)
                if self.hdfs.exists(hdfs_path):
                    with self.hdfs.open(hdfs_path) as f:
                        df = pd.read_csv(f)
                        return df
        except Exception as e:
            print(str(e))

    def read_files(self, file_names):
        raise Exception("Not implemented")

    def write_file(self, source_file, file_name):
        try:
            for data_type in self.import_types.keys():
                if data_type in source_file:
                    dest_path = self.hdfs_types[data_type]
                    # pushing to HDFS
                    self.hdfs.put(source_file, os.path.join(dest_path, file_name))
                    print(f"Write to file: {os.path.join(dest_path, file_name)}")
        except Exception as e:
            print(str(e))


# Test Functions
# if __name__ == "__main__":
    # hdfUtil = HDFSUtil()
    #     hdfUtil.import_local_data()
    # hdfUtil.delete_file("temp_tweet.csv")
#     df = hdfUtil.read_file_from_hdfs('tweets_08-03-2020.csv')
#     df.info()
