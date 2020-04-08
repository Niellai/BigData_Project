import React, { useState, useEffect } from "react";
import DataBox from "../components/DataBox";
import Loader from "../components/Loader";
import sampleTags from "../data/sampleTags";
import SearchBar from "../components/SearchBar";
import { convertDate, getQuery } from "../common";

const transformTag = (tag, index) => {
  const { author, date, doc, score, sentence } = tag;

  const trimSentence = sentence.trim();
  const Content = doc.replace(
    trimSentence,
    `<span style="background-color: white; color: black; border-radius: 5px; padding: 0 2px;">${trimSentence}</span>`
  );
  const formattedDate = date
    .split("_")[0]
    .split("-")
    .reverse()
    .join("-")
    .concat(`T${date.split("_")[1]}`);
  return {
    index,
    author,
    Content,
    Date: parseInt((new Date(formattedDate).getTime() / 1000).toFixed(0)),
    compound: score,
    label: score > 0 ? 1 : score < 0 ? -1 : 0,
  };
};

const ScreensTag = ({ setPage, startDate, endDate }) => {
  const [boxClass, setBoxClass] = useState("main-box");
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState("");
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);

  const onSubmit = () => {
    setLoading(true);

    const timeout = process.env.REACT_APP_MODE === "DEV" ? 3000 : 0;
    setTimeout(async () => {
      if (process.env.REACT_APP_MODE === "DEV") {
        setResults(sampleTags.result);
      } else {
        const start_date = convertDate(startDate);
        const end_date = convertDate(endDate);
        const context = tags.join(",");
        const returnData = await getQuery(start_date, end_date, context, query);

        console.log(returnData);
        setResults(returnData.result);
        setTags([]);
        setQuery("");
      }
      setTimeout(() => setLoading(false), 100);
    }, timeout);
  };

  useEffect(() => {
    setTimeout(() => setBoxClass("main-box expanded is-visible"));
  }, []);

  // props
  const searchProps = { query, setQuery, tags, setTags, onSubmit };
  return (
    <div className="content-container">
      <div className={boxClass}>
        {!loading ? (
          <>
            <div className="box-menu">
              <div className="box-title">#tags</div>
              <div className="box-back" onClick={() => setPage("main")}>
                <i className="fas fa-chevron-circle-left"></i>
              </div>
            </div>
            <div className="box-container column">
              <SearchBar {...searchProps} />
              <div className="bar-container column scroll expanded">
                <div className="title">Searched Documents</div>
                {!loading && results.length !== 0 && (
                  <>
                    {results
                      .map((tag, num) => transformTag(tag, num))
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

export default ScreensTag;
