import React, { useState, useEffect, useRef } from "react";
import Bar from "../components/Bar";
import WordCloud from "../components/WordCloud";
import wcData from "../data/sampleWordcloud";
import sampleData from "../data/sampleBar";
import Loader from "../components/Loader";

const ScreensWordCloud = ({ setPage }) => {
  const containerRef = useRef(null);
  const [boxClass, setBoxClass] = useState("main-box");
  const [loading, setLoading] = useState(true);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    setTimeout(() => setBoxClass("main-box expanded"));
    setTimeout(() => {
      setLoading(false);
      setTimeout(() => setBoxClass("main-box expanded is-visible"), 200);
      setTimeout(() => setLoaded(true), 500);
    }, 3000);
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
                <Bar data={sampleData} />
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
