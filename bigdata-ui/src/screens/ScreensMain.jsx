import React from "react";

const ScreensMain = ({ setPage }) => {
  return (
    <div className="main-container">
      <div className="main-box" onClick={() => setPage("sentiment")}>
        <div className="box-title">#sentiments</div>
        <div className="box-icon">
          <i className="far fa-laugh-squint"></i>
        </div>
        <div className="box-description">
          Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quibusdam
          excepturi earum ratione, incidunt dolorum fugiat amet, deserunt rem
          dolore quidem atque quam nemo vel explicabo corrupti odit laborum
          aperiam velit?
        </div>
        <div className="box-brands">
          <i className="fab fa-twitter-square"></i>
          <i className="fas fa-rss-square"></i>
        </div>
      </div>
      <div className="main-box" onClick={() => setPage("wordcloud")}>
        <div className="box-title">#wordcloud</div>
        <div className="box-icon">
          <i className="fab fa-contao"></i>
        </div>
        <div className="box-description">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Soluta
          deserunt assumenda quaerat cupiditate? Maiores officia mollitia
          nesciunt enim. Illum ullam deleniti dolores excepturi modi enim dicta
          minus nam, et repudiandae!
        </div>
        <div className="box-brands">
          <i className="fab fa-twitter-square"></i>
          <i className="fas fa-rss-square"></i>
        </div>
      </div>
      <div className="main-box">
        <div className="box-title">#tags</div>
        <div className="box-icon">
          <i className="fas fa-tags"></i>
        </div>
        <div className="box-description">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Incidunt
          porro expedita magni error aliquam voluptatum quisquam saepe odit non
          eveniet dolores laboriosam voluptatem autem facere vitae, ratione
          tempora soluta delectus?
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
