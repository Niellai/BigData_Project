import React, { useState, useEffect } from "react";
import Bar from "../components/Bar";
import WordCloud from "../components/WordCloud";
import sampleData from "../data/sampleBar";

const ScreensWordCloud = ({ setPage }) => {
  const [boxClass, setBoxClass] = useState("main-box");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => setBoxClass("main-box expanded"));
    setTimeout(() => setLoading(false), 1000);
  }, []);
  return (
    <div className="content-container">
      <div className={boxClass}>
        <div className="box-menu">
          <div className="box-title">#wordcloud</div>
          <div className="box-back" onClick={() => setPage("main")}>
            <i className="fas fa-chevron-circle-left"></i>
          </div>
        </div>
        <div className="box-container">
          <div className="bar-container">
            {!loading && <Bar data={sampleData} />}
          </div>
          <div className="bar-container">{!loading && <WordCloud />}</div>
        </div>
      </div>
    </div>
  );
};

export default ScreensWordCloud;
