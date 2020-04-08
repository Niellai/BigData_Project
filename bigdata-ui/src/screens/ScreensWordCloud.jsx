import React, { useState, useEffect, useRef } from "react";
import Bar from "../components/Bar";
import WordCloud from "../components/WordCloud";
import sampleWcData from "../data/sampleWordcloud";
import Loader from "../components/Loader";
import { getWordCloud, convertDate } from "../common";

const transformToBarData = (data) => {
  const intData = Object.keys(data).map((i) => ({
    [i]: data[i],
    count: data[i],
    word: i,
  }));
  intData.sort((a, b) => b.count - a.count);
  const slicedData = intData.slice(0, 20);
  slicedData.sort((a, b) => a.count - b.count);
  const keyData = slicedData.map((i) => i.word);
  const barData = slicedData.map((i, num) => {
    delete i["count"];
    delete i["word"];
    return { ...i, index: num };
  });
  return {
    barData: barData,
    keyData: keyData,
  };
};

const ScreensWordCloud = ({ setPage, startDate, endDate }) => {
  const containerRef = useRef(null);
  const [wcData, setWcData] = useState({});
  const [boxClass, setBoxClass] = useState("main-box");
  const [loading, setLoading] = useState(true);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    setTimeout(() => setBoxClass("main-box expanded"));
    const timeout = process.env.REACT_APP_MODE === "DEV" ? 3000 : 0;
    setTimeout(async () => {
      if (process.env.REACT_APP_MODE === "DEV") {
        setWcData(sampleWcData);
      } else {
        const start_date = convertDate(startDate);
        const end_date = convertDate(endDate);
        const returnData = await getWordCloud(start_date, end_date);
        setWcData(returnData);
      }
      setTimeout(() => setLoading(false), 100);
      setTimeout(() => setBoxClass("main-box expanded is-visible"), 300);
      setTimeout(() => setLoaded(true), 600);
    }, timeout);
  }, []);

  return (
    <div className="content-container">
      <div className={boxClass}>
        {!loading ? (
          <>
            <div className="box-menu">
              <div className="box-title">#wordcloud</div>
              <div className="box-back" onClick={() => setPage("main")}>
                <i className="fas fa-chevron-circle-left"></i>
              </div>
            </div>
            <div className="box-container">
              <div className="bar-container">
                <Bar data={transformToBarData(wcData)} />
              </div>
              <div className="bar-container" ref={containerRef}>
                {loaded && (
                  <WordCloud
                    data={wcData}
                    containerWidth={containerRef.current.clientWidth}
                  />
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

export default ScreensWordCloud;
