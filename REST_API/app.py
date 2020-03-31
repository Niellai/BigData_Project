from json import dumps
import json
from flask import Flask, request
from datetime import date

from kafka import KafkaProducer
from BigData_Project.NLPAnalytics.SampleNLP import SampleNLP

sampleNLP = SampleNLP()

app = Flask(__name__)


@app.route('/')
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

        result = sampleNLP.word_cloud(mDate)
        return result


if __name__ == '__main__':
    app.run()
