import React, { useState, useEffect } from "react";
import CountUp from "react-countup";

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
          <div className="box-title">#sentiments</div>
          <div className="box-back" onClick={() => setPage("main")}>
            <i className="fas fa-chevron-circle-left"></i>
          </div>
        </div>
        <div className="box-container">
          <div className="bar-container">
            {!loading && (
              <div className="sentiment-number">
                <CountUp
                  start={0}
                  end={30}
                  duration={2.75}
                  separator=" "
                  decimal=","
                  prefix="+"
                  suffix="%"
                />
              </div>
            )}
          </div>
          <div className="bar-container column scroll">
            {!loading && (
              <>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
                <div className="box-data"></div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScreensWordCloud;