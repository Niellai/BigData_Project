import React from "react";
import DOMPurify from "dompurify";

const convertDate = (date) => {
  return date
    .toISOString()
    .split("T")
    .join(" ")
    .split(":")
    .slice(0, 2)
    .join(":");
};

const DataBox = ({ data }) => {
  const date = new Date(data.Date);
  const displayDate = convertDate(date);
  const emoticon =
    data.label === 0 ? "meh" : data.label === 1 ? "smile" : "angry";
  const sentimentClass = `fas fa-${emoticon} mr-1`;
  return (
    <div className="box-data" key={data.index}>
      <div className="box-data-date"></div>
      <div className="box-data-header">
        <div className="box-data-user">
          <i className="fas fa-user-tie mr-1"></i>
          {data.author}
        </div>
        <div className="box-data-date">
          <i className="fas fa-calendar mr-1"></i>
          {displayDate}
        </div>
      </div>
      <div
        className="box-data-text"
        dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(data.Content) }}
      />
      <div className={`box-data-sentiment ${emoticon}`}>
        <i className={sentimentClass}></i>
        {Math.abs((data.compound * 100).toFixed(0))}%
      </div>
    </div>
  );
};

export default DataBox;
