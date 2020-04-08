import React from "react";
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

const UIDatePicker = ({ date = new Date(), setDate }) => {
  return (
    <DatePicker
      selected={date}
      onChange={(date) => setDate(date)}
      // showTimeSelect
      // timeFormat="HH:mm"
      // timeIntervals={30}
      // dateFormat="MMM d, yyyy @ kk:mm:ss.000"
    />
  );
};

export default UIDatePicker;
