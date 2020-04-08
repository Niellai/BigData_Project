import React from "react";
import LoaderSvg from "../loading.svg";

const Loader = () => {
  return (
    <div className="loader-container">
      <img src={LoaderSvg} alt="Loading" />
      <div className="loader-text">Calling API from Flask...</div>
    </div>
  );
};

export default Loader;
