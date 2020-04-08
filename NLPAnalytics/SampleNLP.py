import json
import os
import re

import gensim.downloader as api
import numpy as np
import spacy
from gensim.utils import tokenize
from pyspark import SparkContext, SQLContext
from dateutil import parser
import pandas as pd

from BigData_Project.HDFS.HDFSUtil import HDFSUtil

java8_location = '/usr/lib/jvm/java-8-openjdk-amd64'  # Set your own
os.environ['JAVA_HOME'] = java8_location


class SampleNLP(object):
    """
    Fixing JAVA version issue: https://stackoverflow.com/questions/53583199/pyspark-error-unsupported-class-file-major-version-55
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.hdfsUtil = HDFSUtil()
        self.df, self.df_schema = self.hdfsUtil.read_file_dataframe("tweets_20-02-2020.csv")
        self.model = api.load("glove-wiki-gigaword-50", return_path=False)

        # SparkCode
        sc = SparkContext.getOrCreate()
        self.sqlContext = SQLContext(sc)
        self.vector_list = []

    def spark_word_cloud(self, data, max_row=500):
        """
        Faster extract tokens and count them. Will look for both tweet and rss.
        :param max_row: Limit number of rows to extract
        :return: count token dictionary
        """
        start_date = data['start_date']
        if "end_date" in data.keys():
            end_date = data['end_date']
        else:
            end_date = None

        # Loading from Tweets
        sample_text1 = ""
        tweet_df, tweet_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date,
                                                                 data_type='tweet')
        if tweet_df is not None or tweet_df_schema is not None:
            tweet_df = self.sqlContext.createDataFrame(tweet_df, tweet_df_schema)
            sample_text1 = " ".join(
                text.text for text in tweet_df.select("text").rdd.takeSample(False, max_row, seed=42))

        # Loading from RSS
        sample_text2 = ""
        rss_df, rss_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date, data_type='rss')
        if rss_df is not None or rss_df_schema is not None:
            rss_df = self.sqlContext.createDataFrame(rss_df, rss_df_schema)
            sample_text2 = " ".join(
                text.title for text in rss_df.select("title").rdd.takeSample(False, max_row, seed=42))

        sample_text = f"{sample_text1} {sample_text2}"

        # Extract tokens
        doc = self.nlp(sample_text)
        tokens = [str(token.lemma_.lower()) for token in doc if not token.is_stop
                  and not token.is_punct
                  and not token.is_space
                  and len(token) >= 3
                  and not token.like_url
                  and token.is_alpha]

        # Count tokens
        token_dic = {}
        token_set = set(tokens)
        for t in token_set:
            token_dic[t] = 0

        for t in tokens:
            token_dic[t] += 1

        return token_dic

    def word_cloud(self, data):
        start_date = data['start_date']
        if "end_date" in data.keys():
            end_date = data['end_date']
        else:
            end_date = None
        self.df = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date, data_type='tweet')

        if self.df is None:
            return {'status': "200", "message": "No file found"}

        tokens = []
        for idx, row in self.df.iterrows():
            doc = self.nlp(row['text'])
            for token in doc:
                if token.is_alpha and not token.is_stop:
                    tokens.append(token.text)

        token_dic = {}
        token_set = set(tokens)
        for t in token_set:
            token_dic[t] = 0

        for t in tokens:
            token_dic[t] += 1

        return token_dic

    def contain_word(self, word):
        return word in self.model.vocab.keys()

    def sentence_vector(self, sentence, negative=None, positive=None):
        """
        Use either negative or positive sentences to guide sentence vector
        """
        if negative:
            negative = list(tokenize(negative))
            negative = [word for word in negative if word not in sentence]
            # print(negative)
            neg_vectors = [self.model[word] for word in negative if self.contain_word(word)]

            # tokenize sentence, we need sentence as a string to extract additional words in negative
            sentence = list(tokenize(sentence))
            vectors = [self.model[word] for word in sentence if self.contain_word(word)]
            vectors = np.mean(vectors, axis=0)

            if len(neg_vectors) == 0:
                neg_vectors = np.zeros(vectors.shape)

            return vectors - np.mean(neg_vectors, axis=0)

        elif positive:
            positive = list(tokenize(positive))
            positive = [word for word in positive if word not in sentence]
            # print(positive)
            pos_vectors = [self.model[word] for word in positive if self.contain_word(word)]

            # tokenize sentence, we need sentence as a string to extract additional words in positive
            sentence = list(tokenize(sentence))
            vectors = [self.model[word] for word in sentence if self.contain_word(word)]
            vectors = np.mean(vectors, axis=0)

            if len(pos_vectors) == 0:
                pos_vectors = np.zeros(vectors.shape)

            return vectors + np.mean(pos_vectors, axis=0)

        else:
            sentence = list(tokenize(sentence))
            vectors = [self.model[word] for word in sentence if self.contain_word(word)]
            if not vectors:
                return np.zeros(50)
            return np.mean(vectors, axis=0)

    def search_doc(self, query, context=None, top_n=3):
        try:
            # get the top result in dataframe
            query_vector = self.sentence_vector(query, positive=context)
            # result = self.model.cosine_similarities(query_vector, [v for v in self.df['vector'].values])
            result = self.model.cosine_similarities(query_vector, self.vector_list)
            self.df['score'] = result
            top_result = self.df.sort_values('score', ascending=False)[:top_n]

            # get the closes sentences
            final_result = {}
            result = []
            for idx, row in top_result.iterrows():
                meta = {}
                sents = self.nlp(row['text']).sents
                sents = list(sents)
                sents_vectors = []
                for sent in sents:
                    vector = self.sentence_vector(str(sent))
                    sents_vectors.append(vector)
                scores = self.model.cosine_similarities(query_vector, sents_vectors)
                scores[np.isnan(scores)] = 0

                datetime = parser.parse(str(row['date']))
                meta["sentence"] = str(sents[int(np.argmax(scores))])
                meta["score"] = str(scores[np.argmax(scores)])
                meta["doc"] = str(row['text'])
                meta['date'] = str(datetime.strftime("%d-%m-%Y_%H:%M:%S"))
                meta['author'] = str(row['source'])

                result.append(meta)
            final_result['result'] = result
            result_str = json.dumps(final_result)
            result_str = result_str.encode('utf8')
            return re.sub(rb'[^\x00-\x7f]', rb' ', result_str)
        except Exception as e:
            return "No result."

    def query_sentence(self, data):
        start_date = data['start_date']
        if "end_date" in data.keys():
            end_date = data['end_date']
        else:
            end_date = None

        query = data['query']
        if "context" in data.keys():
            context = data['context']
        else:
            context = None

        if "top_n" in data.keys():
            top_n = data['top_n']
        else:
            top_n = 3

        # LOADING tweets
        sample_size = 5000
        self.vector_list = []
        df_tweet, tweet_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date,
                                                                 data_type='tweet')
        if df_tweet is None:
            df_tweet = pd.DataFrame()
        else:
            if len(df_tweet) > sample_size:
                df_tweet = df_tweet.sample(n=sample_size)

            # compute tweet document vectors
            for doc in df_tweet['text']:
                vector = self.sentence_vector(doc)
                self.vector_list.append(vector)

            df_tweet = df_tweet[["text", "screen_name", "created_at"]]
            df_tweet.columns = ['text', "source", "date"]

        # LOADING rss
        df_rss, res_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date, data_type="rss")
        if df_rss is not None:
            # df_rss = df_rss.sample(n=sample_size)
            # compute rss document vectors
            for doc in df_rss['title']:
                vector = self.sentence_vector(doc)
                self.vector_list.append(vector)

            df_rss = df_rss[['title', 'link', 'published']]
            df_rss.columns = ['text', "source", "date"]
        else:
            df_rss = pd.DataFrame()

        # No result found
        if len(df_tweet) == 0 and len(df_rss) == 0:
            return "{}"

        # Combine tweet and rss into single data frame
        self.df = pd.concat([df_tweet, df_rss])

        # Search for  the closet document
        return self.search_doc(query, context, top_n)

    def get_sentiment(self, data):
        start_date = data['start_date']
        if "end_date" in data.keys():
            end_date = data['end_date']
        else:
            end_date = None

        is_positive = data['is_positive']
        top_n = data['top_n']

        df_tweet, tweet_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date,
                                                                 data_type='tweet')
        sample_size = 10000
        if df_tweet is not None and len(df_tweet) > sample_size:
            df_tweet = df_tweet.sample(n=sample_size)

        if "compound" in list(df_tweet.columns) and is_positive:
            df_result = df_tweet.sort_values(by=['compound'], ascending=False)[:top_n]
        else:
            df_result = df_tweet.sort_values(by=['compound'], ascending=True)[:top_n]

        df_result = df_result[["text", "screen_name", "created_at", "compound"]]
        return df_result.to_json(orient="records")

# if __name__ == "__main__":
#     try:
#         sampleNLP = SampleNLP()
#         sampleNLP.spark_word_cloud()
#     except Exception as e:
#         print(str(e))
# data = {'start_date': "20-02-2020"}
# tokens = sampleNLP.word_cloud(data)
