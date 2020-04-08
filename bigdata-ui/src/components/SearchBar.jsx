import React from "react";
import CreatableSelect from "react-select/creatable";
import { colourOptions } from "../options";
import makeAnimated from "react-select/animated";

const animatedComponents = makeAnimated();

const SearchBar = ({ query, setQuery, setTags, onSubmit }) => {
  const handleChange = (input) => {
    setTags(input.map((i) => i.label));
  };
  return (
    <div className="box-search">
      <div className="box-inputs">
        <input
          className="box-search-input"
          type="text"
          placeholder="Please Type in your Query here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <CreatableSelect
          isMulti
          components={animatedComponents}
          name="colors"
          options={colourOptions}
          className="basic-multi-select"
          classNamePrefix="select"
          onChange={handleChange}
        />
      </div>
      <button className="box-search-button" onClick={onSubmit}>
        Search
      </button>
    </div>
  );
};

export default SearchBar;
