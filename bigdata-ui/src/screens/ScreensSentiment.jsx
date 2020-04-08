import React, { useState, useEffect } from "react";
import CountUp from "react-countup";
import DataBox from "../components/DataBox";
import Loader from "../components/Loader";
import sampleOverall from "../data/sampleOverallSentiment";
import sampleSentiment from "../data/sampleSentiment";

const ScreensSentiment = ({ setPage }) => {
  const [boxClass, setBoxClass] = useState("main-box");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => setBoxClass("main-box expanded"));
    setTimeout(() => {
      setLoading(false);
      setTimeout(() => setBoxClass("main-box expanded is-visible"), 200);
    }, 3000);
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
                {sampleSentiment.map((i) => (
                  <DataBox data={i} key={i.index} />
                ))}
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
