import React, { useState } from "react";
import ScreensMain from "./ScreensMain";
import Background from "../components/Background";
import ScreensSentiment from "./ScreensSentiment";
import ScreensWordCloud from "./ScreensWordCloud";

const ScreensRoot = () => {
  const [page, setPage] = useState("main");

  return (
    <div>
      <Background />
      <div className="content">
        <div className="main">
          <div className="main-container">
            <div className="main-title">#coronavirus</div>
          </div>
          {page === "main" && <ScreensMain setPage={setPage} />}
          {page === "sentiment" && <ScreensSentiment setPage={setPage} />}
          {page === "wordcloud" && <ScreensWordCloud setPage={setPage} />}
        </div>
      </div>
    </div>
  );
};

export default ScreensRoot;
