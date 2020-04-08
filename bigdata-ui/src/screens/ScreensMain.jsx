import React from "react";

const ScreensMain = ({ setPage }) => {
  return (
    <div className="main-container">
      <div className="main-box is-visible" onClick={() => setPage("sentiment")}>
        <div className="box-title">#sentiments</div>
        <div className="box-icon">
          <i className="far fa-laugh-squint"></i>
        </div>
        <div className="box-description">
          Find out more about the public sentiment on COVID-19, what incident
          made everyone most upset and what events gave them hope. Sentiment
          Analysis is the process of determining whether a piece of writing
          (product/movie review, tweet, etc.) is positive, negative or neutral.
        </div>
        <div className="box-brands">
          <i className="fab fa-twitter-square"></i>
          <i className="fas fa-rss-square"></i>
        </div>
      </div>
      <div className="main-box is-visible" onClick={() => setPage("wordcloud")}>
        <div className="box-title">#wordcloud</div>
        <div className="box-icon">
          <i className="fab fa-contao"></i>
        </div>
        <div className="box-description">
          Find out what is the most important and common topic of interest
          during a certain period of COVID-19 pandemic.  WordCloud is an image
          composed of words used in a particular text or subject, in which the
          size of each word indicates its frequency or importance.” So, the more
          often a specific word appears in your text, the bigger and bolder it
          appears in your word cloud.
        </div>
        <div className="box-brands">
          <i className="fab fa-twitter-square"></i>
          <i className="fas fa-rss-square"></i>
        </div>
      </div>
      <div className="main-box is-visible" onClick={() => setPage("tag")}>
        <div className="box-title">#tags</div>
        <div className="box-icon">
          <i className="fas fa-tags"></i>
        </div>
        <div className="box-description">
          Query tags allow you to search for a couple of similar Twitter post.
          This will help to gain insight on how to overall sentiments of the
          general public, where it can be further use for a specific business
          use case. The most recent research builds on our prior work
          demonstrating that Twitter provides meaningful knowledge about
          strategic outcomes, identifying potential policy remedies, and
          describing the likely impact of proposed policy interventions.
        </div>
        <div className="box-brands">
          <i className="fab fa-twitter-square"></i>
          <i className="fas fa-rss-square"></i>
        </div>
      </div>
    </div>
  );
};

export default ScreensMain;
