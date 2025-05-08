// src/components/TimelineLayout.jsx

import TimelineEvent from "./TimelineEvent";
import SupplementaryCard from "./SupplementaryCard";

export default function TimelineLayout({ data }) {
  return (
    <div className="px-6 py-10 max-w-4xl mx-auto space-y-10">

      {/* Header */}
      <div className="bg-gray-100 p-6 rounded-xl shadow-md text-center">
        <div className="w-16 h-16 bg-purple-300 text-white font-bold rounded-full flex items-center justify-center mx-auto text-2xl">
          {data.title.split(" ")[0][0]}{data.title.split(" ")[1][0]}
        </div>
        <h1 className="text-2xl font-bold text-gray-800 mt-3">{data.title}</h1>
        <p className="text-sm text-gray-600 mt-1">{data.subtitle}</p>
        {data.tags && (
          <div className="flex flex-wrap justify-center gap-2 mt-3">
            {data.tags.map((tag, idx) => (
              <span
                key={idx}
                className="text-xs bg-white border text-purple-700 px-2 py-1 rounded-full shadow-sm"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Timeline */}
      <div className="relative pl-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Gatsby’s Timeline</h2>
        <div className="ml-2">
          {data.events.map((e, idx) => (
            <TimelineEvent key={idx} event={e} />
          ))}
        </div>
      </div>

      {/* Supplementary explanation */}
      {data.supplementary && (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          {data.supplementary.map((item, idx) => (
            <SupplementaryCard key={idx} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
