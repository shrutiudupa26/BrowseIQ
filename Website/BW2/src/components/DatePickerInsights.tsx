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
      // Convert date to YYYY-MM-DD string
      const yyyy_mm_dd = date.toISOString().split('T')[0];
      const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8001';
      try {
        const response = await fetch(`${BACKEND_URL}/api/query_history_by_date`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ date: yyyy_mm_dd }),
        });
        const data = await response.json();
        setInsights(data.result || 'No insights available for this date.');
      } catch (err) {
        setInsights('Failed to fetch insights.');
      }
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