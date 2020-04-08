import React from "react";
import CreatableSelect from "react-select/creatable";
import { colourOptions } from "../options";
import makeAnimated from "react-select/animated";

const animatedComponents = makeAnimated();

const SearchBar = ({ query, setQuery, tags, setTags }) => {
  return (
    <div className="box-search">
      <div className="box-inputs">
        <input
          className="box-search-input"
          type="text"
          placeholder="Please Type in your Query here..."
        />
        <CreatableSelect
          isMulti
          components={animatedComponents}
          name="colors"
          options={colourOptions}
          className="basic-multi-select"
          classNamePrefix="select"
        />
      </div>
      <button className="box-search-button">Search</button>
    </div>
  );
};

export default SearchBar;
