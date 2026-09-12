import React from 'react';

const OfflineIndicator = () => {
  return (
    <div className="bg-yellow-600 text-white px-4 py-2 text-center font-semibold sticky top-0 z-50">
      📡 You are offline - Using cached data (30-day cache available)
    </div>
  );
};

export default OfflineIndicator;
