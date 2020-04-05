import os
import re

import spacy
from gensim.utils import tokenize
from pyspark import SparkContext, SQLContext
import gensim.downloader as api
import numpy as np
import pandas as pd
from flask import jsonify
import json

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

    def spark_word_cloud(self, data, max_row=1000):
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

        # load data from hdfs
        tweet_df, tweet_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date,
                                                                 data_type='tweet')
        tweet_df = self.sqlContext.createDataFrame(tweet_df, tweet_df_schema)

        rss_df, rss_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date, data_type='rss')
        rss_df = self.sqlContext.createDataFrame(rss_df, rss_df_schema)

        sample_text1 = " ".join(text.text for text in tweet_df.select("text").rdd.takeSample(False, max_row, seed=42))
        sample_text2 = " ".join(text.title for text in rss_df.select("title").rdd.takeSample(False, max_row, seed=42))
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

                meta["sentence"] = str(sents[int(np.argmax(scores))])
                meta["score"] = str(scores[np.argmax(scores)])
                meta["doc"] = str(row['text'])
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

        # load data from hdfs
        self.df, tweet_df_schema = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date,
                                                                data_type='tweet')
        if len(self.df) > 10000:
            self.df = self.df.sample(n=10000)

        # compute document vectors
        self.vector_list = []
        for doc in self.df['text']:
            vector = self.sentence_vector(doc)
            self.vector_list.append(vector)

        # Search for  the closet document
        return self.search_doc(query, context, top_n)

# if __name__ == "__main__":
#     try:
#         sampleNLP = SampleNLP()
#         sampleNLP.spark_word_cloud()
#     except Exception as e:
#         print(str(e))
# data = {'start_date': "20-02-2020"}
# tokens = sampleNLP.word_cloud(data)
