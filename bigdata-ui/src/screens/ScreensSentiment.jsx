import React, { useState, useEffect } from "react";
import CountUp from "react-countup";
import DataBox from "../components/DataBox";
import Loader from "../components/Loader";
import sampleOverall from "../data/sampleOverallSentiment";
import sampleSentiment from "../data/sampleSentiment";

const data = [
  {
    index: 566,
    Content:
      '<span style="background-color: white; color: black; border-radius: 5px; padding: 0 2px;">@sighpad Good</span> thread ðŸ‘ðŸ½ðŸ‘ðŸ½...we need to start taking this more seriously, recently i took the bus and there was a paâ€¦ https://t.co/XnuAj5rgbY',
    author: "Kenneth Ong",
    label: 1,
    compound: 0.6124,
    published_date: "Sun",
    Date: 1582425603000,
  },
  {
    index: 567,
    Content:
      "@sighpad Good thread ðŸ‘ðŸ½ðŸ‘ðŸ½...we need to start taking this more seriously, recently i took the bus and there was a paâ€¦ https://t.co/XnuAj5rgbY",
    author: "Cougher Cheong",
    label: -1,
    compound: -0.55,
    published_date: "Sun",
    Date: 1582425603000,
  },
];

const ScreensWordCloud = ({ setPage }) => {
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

export default ScreensWordCloud;
