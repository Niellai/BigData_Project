import React, { useState, useEffect } from "react";
import CountUp from "react-countup";
import DataBox from "../components/DataBox";
import Loader from "../components/Loader";
import sampleOverall from "../data/sampleOverallSentiment";
import sampleSentiment from "../data/sampleSentiment";
import { convertDate, getExtreme } from "../common";

const transformSentiment = (sentiment, index) => {
  if (process.env.REACT_APP_MODE === "DEV") {
    return sentiment;
  } else {
    const { screen_name, compound, text, created_at } = sentiment;
    return {
      index,
      compound,
      author: screen_name,
      Content: text,
      Date: parseInt(new Date(created_at).getTime().toFixed(0)),
      label: compound > 0 ? 1 : compound < 0 ? -1 : 0,
    };
  }
};

const ScreensSentiment = ({ setPage, startDate, endDate }) => {
  const [results, setResults] = useState([]);
  const [boxClass, setBoxClass] = useState("main-box");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => setBoxClass("main-box expanded"));
    const timeout = process.env.REACT_APP_MODE === "DEV" ? 3000 : 0;
    setTimeout(async () => {
      if (process.env.REACT_APP_MODE === "DEV") {
        setResults(sampleSentiment);
      } else {
        const start_date = convertDate(startDate);
        const end_date = convertDate(endDate);
        const returnData = await getExtreme(start_date, end_date, false);

        setResults(returnData.result);
      }
      setTimeout(() => setLoading(false), 100);
      setTimeout(() => setBoxClass("main-box expanded is-visible"), 300);
    }, timeout);
  }, []);
  return (
    <div className="content-container">
      <div className={boxClass}>
        {!loading ? (
          <>
            <div className="box-menu">
              <div className="box-title">#sentiments</div>
              <div className="box-back" onClick={() => setPage("main")}>
                <i className="fas fa-chevron-circle-left"></i>
              </div>
            </div>
            <div className="box-container">
              <div className="bar-container gray rounded padded">
                <div>
                  <div className="sentiment-number">
                    <CountUp
                      start={0}
                      end={Math.abs(
                        (sampleOverall.overall_sentiment * 100).toFixed(0)
                      )}
                      delay={0.8}
                      duration={2.75}
                      separator=" "
                      decimal=","
                      prefix={sampleOverall > 0 ? "+" : "-"}
                      suffix="%"
                    />
                    <div className="title">Overall Sentiment</div>
                  </div>
                </div>
              </div>
              <div className="bar-container column scroll gray rounded padded">
                <div className="title">Extreme Sentiment Documents</div>
                {!loading && results.length !== 0 && (
                  <>
                    {results
                      .map((sentiment, num) =>
                        transformSentiment(sentiment, num)
                      )
                      .map((i) => (
                        <DataBox data={i} key={i.index} />
                      ))}
                  </>
                )}
              </div>
            </div>
          </>
        ) : (
          <Loader />
        )}
      </div>
    </div>
  );
};

export default ScreensSentiment;
