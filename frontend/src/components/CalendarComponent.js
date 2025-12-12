import React from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './CalendarComponent.css';

const CalendarComponent = ({ selectedDate, onDateChange, markedDates = [], minDate }) => {
  // Check if a date has bookings
  const hasBookings = (date) => {
    return markedDates.some(
      (markedDate) =>
        new Date(markedDate).toDateString() === date.toDateString()
    );
  };

  // Add custom class to dates with bookings
  const tileClassName = ({ date, view }) => {
    if (view === 'month' && hasBookings(date)) {
      return 'has-bookings';
    }
    return null;
  };

  return (
    <div className="calendar-container">
      <Calendar
        onChange={onDateChange}
        value={selectedDate}
        minDate={minDate || new Date()}
        tileClassName={tileClassName}
        className="custom-calendar"
      />
    </div>
  );
};

export default CalendarComponent;
