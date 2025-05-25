// src/components/DatePickerInsights.tsx
import React, { useState, useRef, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const DatePickerInsights: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [insights, setInsights] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleDateChange = async (date: Date | null) => {
    setSelectedDate(date);
    if (date) {
      const timestamp = date.getTime(); // Convert date to timestamp
      // Call the backend API to get browsing insights
      const response = await fetch(`/api/analytics?timestamp=${timestamp}`);
      const data = await response.json();
      setInsights(data.insights); // Assuming the response has an 'insights' field
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [insights]);

  return (
    <div className="date-picker-insights flex items-start gap-8">
      <div>
        <h2 className="mb-2 font-semibold">Choose a Date to See Insights</h2>
        <DatePicker
          selected={selectedDate}
          onChange={handleDateChange}
          dateFormat="yyyy/MM/dd"
          className="w-48 bg-gray-900 text-white border border-gray-700 rounded p-2"
          popperPlacement="bottom-start"
        />
      </div>
      <div className="insights-box flex-1">
        {selectedDate && (
          <p className="mb-2">
            Jane Doe's browsing patterns for {selectedDate.toLocaleDateString()}:
          </p>
        )}
        <textarea
          ref={textareaRef}
          value={insights}
          readOnly
          placeholder="Insights will be displayed here..."
          className="w-full min-h-[80px] max-h-96 resize-none bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white border-2 border-transparent focus:border-orange-400 focus:ring-2 focus:ring-purple-500 rounded-xl p-4 shadow-lg font-mono text-base transition-all duration-300 ease-in-out scrollbar-thin scrollbar-thumb-orange-400 scrollbar-track-gray-800"
          style={{ overflowY: 'auto', boxShadow: '0 4px 24px 0 rgba(80, 0, 120, 0.15)' }}
        />
      </div>
    </div>
  );
};

export default DatePickerInsights;