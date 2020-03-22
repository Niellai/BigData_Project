from json import loads, dumps

import spacy
from bs4 import BeautifulSoup
from kafka import KafkaConsumer, KafkaProducer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class CleanSentiment(object):
    def __init__(self):
        super().__init__()

        # listen to topic from LiveTweet.py
        self.is_listening = True
        self.listen_topic = "transformed_tweet"
        self.consumer = KafkaConsumer(
            self.listen_topic,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        # initial Kafka producer
        self.send_topic = "sentiment_tweet"
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

        self.nlp = spacy.load("en_core_web_sm")
        self.analyser = SentimentIntensityAnalyzer()

    def sentiment_analyzer_scores(self, sentence, is_print=False):
        score = self.analyser.polarity_scores(sentence)
        if is_print:
            print("{:-<40} {}".format(sentence, str(score)))
        return score

    def get_sentiment(self, doc):
        total_scores = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}

        # Convert document to sentences and remove special chars, symbols, etc
        for sent in doc.sents:
            sent = str(sent)
            soup = BeautifulSoup(sent, 'lxml')
            html_free = soup.get_text()
            scores = self.sentiment_analyzer_scores(html_free)
            for s in scores.keys():
                total_scores[s] += scores[s]

        # store scores and average them
        for key in total_scores.keys():
            value = total_scores[key]
            value = value / len(list(doc.sents))
            total_scores[key] = value

        return total_scores

    def consume_doc(self):
        while self.is_listening:
            for message in self.consumer:
                # Extracting from consumer
                json_object = message.value
                doc = self.nlp(json_object['text'])

                # Get sentiment
                scores = self.get_sentiment(doc)
                if scores['compound'] > 0.2:
                    sentiment = 1
                elif scores['compound'] < -0.2:
                    sentiment = -1
                else:
                    sentiment = 0

                json_object['sentiment'] = sentiment
                print(json_object)

                # Send to kafka consumer
                self.send_to_kafka(json_object)

    def send_to_kafka(self, data):
        """
        Send sentiment tweet for storing in HDFS

        :return: None
        """
        try:
            self.producer.send(self.send_topic, data)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    cleanText = CleanSentiment()
    cleanText.consume_doc()
    print("Computing sentiment on live tweets...\n")
