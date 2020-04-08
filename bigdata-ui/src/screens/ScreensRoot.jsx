import React, { useState } from "react";
import ScreensMain from "./ScreensMain";
import Background from "../components/Background";
import DateContainer from "../components/DateContainer";
import ScreensSentiment from "./ScreensSentiment";
import ScreensWordCloud from "./ScreensWordCloud";
import ScreensTag from "./ScreensTag";

const ScreensRoot = () => {
  const [page, setPage] = useState("main");

  // set the initial end date to 5 minutes prior
  const initialDate = new Date();
  initialDate.setMinutes(-5);

  // initialize all data
  const [startDate, setStartDate] = useState(new Date("2020-02-20"));
  const [endDate, setEndDate] = useState(new Date("2020-03-27"));
  const [searchDate, setSearchDate] = useState({
    start: initialDate,
    end: new Date(),
  });

  // props
  const dateProps = { startDate, endDate, setStartDate, setEndDate };
  const pageProps = { startDate, endDate, setPage };

  return (
    <div>
      <Background />
      <div className="content">
        <div className="main">
          <div className="main-container column">
            <div className="main-title">#coronavirus</div>
            <DateContainer {...dateProps} />
          </div>
          {page === "main" && <ScreensMain {...pageProps} />}
          {page === "sentiment" && <ScreensSentiment {...pageProps} />}
          {page === "wordcloud" && <ScreensWordCloud {...pageProps} />}
          {page === "tag" && <ScreensTag {...pageProps} />}
        </div>
      </div>
    </div>
  );
};

export default ScreensRoot;
