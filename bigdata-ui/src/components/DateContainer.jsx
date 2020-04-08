import React from "react";
import UIDatePicker from "./DatePicker";

const DateContainer = ({ startDate, setStartDate, endDate, setEndDate }) => {
  return (
    <div className="date-container">
      <div className="calendar-icon">
        <i className="fas fa-calendar-alt"></i>
      </div>
      <UIDatePicker date={startDate} setDate={setStartDate} />
      <div className="arrow-icon">
        <i className="fas fa-arrow-right"></i>
      </div>
      <UIDatePicker date={endDate} setDate={setEndDate} />
    </div>
  );
};

export default DateContainer;
