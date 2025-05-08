// src/components/TimelineEvent.jsx
export default function TimelineEvent({ event }) {
    return (
      <div className="relative pl-10 border-l-4 border-purple-300 mb-8">
        <div className="absolute top-1 left-0 w-5 h-5 bg-purple-400 rounded-full"></div>
        <div className="bg-white rounded-lg shadow-md p-4">
          <p className="text-xs text-purple-700 font-semibold">{event.year}</p>
          <h3 className="text-lg font-bold text-gray-800">{event.event}</h3>
          <p className="text-sm text-gray-600 mt-1">{event.description}</p>
          {event.page && (
            <p className="text-xs text-blue-500 mt-1">Page {event.page}</p>
          )}
        </div>
      </div>
    );
  }
  