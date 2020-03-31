import os

from BigData_Project.HDFS.HDFSUtil import HDFSUtil
import spacy


# java8_location = '/usr/lib/jvm/java-8-openjdk-amd64'  # Set your own
# os.environ['JAVA_HOME'] = java8_location


class SampleNLP(object):
    """
    Fixing JAVA version issue: https://stackoverflow.com/questions/53583199/pyspark-error-unsupported-class-file-major-version-55
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.hdfsUtil = HDFSUtil()
        self.df, _ = self.hdfsUtil.read_file_dataframe("tweets_20-02-2020.csv")

        """ # SparkCode 
        sc = SparkContext.getOrCreate()
        self.sqlContext = SQLContext(sc)

        df = self.sqlContext.createDataFrame(df, df_schema)
        """

    def word_cloud(self, data):
        start_date = data['start_date']
        if "end_date" in data.keys():
            end_date = data['end_date']
        else:
            end_date = None
        self.df = self.hdfsUtil.read_file_date(start_date=start_date, end_date=end_date)

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

# if __name__ == "__main__":
#     sampleNLP = SampleNLP()
#     data = {'start_date': "20-02-2020"}
#     tokens = sampleNLP.word_cloud(data)
