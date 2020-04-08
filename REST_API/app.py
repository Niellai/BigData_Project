from json import dumps
import json
from flask import Flask, request
from datetime import date

from kafka import KafkaProducer
from BigData_Project.NLPAnalytics.SampleNLP import SampleNLP

sampleNLP = SampleNLP()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def CheckService():
    return "Service is running."


@app.route('/WordCloud', methods=['POST'])
def WordCloud():
    """
    Get WordCloud on given specific dates.

    "start_date": Starting date inclusive, have to be in 31-03-2020 format.
    "end_date": Nullable field. Ending date inclusive, have to be in 31-03-2020 format.

    Expected input:
                    { "start_date": 31-03-2020 }

                    { "start_date": 31-03-2020, "end_date": 30-04-2020 }

    :return: Counting of each word. Example {"virus": 55, "lung": 1}
    """
    if request.method == "POST":
        # Extracting from request
        mDate = json.loads(request.data)

        result = sampleNLP.spark_word_cloud(mDate)
        return result


@app.route('/query', methods=['POST'])
def query():
    """
    Query the collected data set by date, query will return top n most similar post back to user.

    Expected input:
    "start_date": "20-02-2020",
    "end_date": "27-03-2020",
    "context": "outbreak, pneumonia",
    "top_n": 3,
    "query": "Find out how #Coronavirus is likely to develop globally."

    :return: Most similar post
    """
    if request.method == "POST":
        data = json.loads(request.data)
        result = sampleNLP.query_sentence(data)
        return json.loads(result)


if __name__ == '__main__':
    app.run()
