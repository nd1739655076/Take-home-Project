// src/components/SummaryCardList.jsx

import SummaryCard from "./SummaryCard";

export default function SummaryCardList({ data }) {
  return (
    <div className="px-6 py-10 max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-purple-800 mb-2">{data.title}</h1>
        <p className="text-sm text-gray-600">Chapter {data.chapter}</p>
      </div>

      {/* Summary Points */}
      <div className="bg-purple-50 rounded-xl p-6 shadow-md">
        <h2 className="text-lg font-semibold text-purple-700 mb-3">Summary</h2>
        <ul className="list-disc pl-6 space-y-2 text-sm text-gray-800">
          {data.summary_points.map((point, idx) => (
            <li key={idx}>{point}</li>
          ))}
        </ul>
      </div>

      {/* Theme */}
      {data.theme && (
        <div className="bg-white rounded-xl p-6 shadow-md text-sm text-gray-800">
          <h2 className="text-md font-semibold text-purple-700 mb-2">Theme</h2>
          <p>{data.theme}</p>
        </div>
      )}
    </div>
  );
}