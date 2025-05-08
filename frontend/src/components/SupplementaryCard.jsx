// src/components/SupplementaryCard.jsx
export default function SupplementaryCard({ item }) {
    return (
      <div className="bg-white p-4 rounded-lg shadow-md text-sm">
        <h4 className="font-semibold text-gray-800 mb-1">{item.title}</h4>
        <p className="text-gray-700">{item.body}</p>
        {item.page && (
          <p className="text-xs text-blue-500 mt-2">Go to page {item.page}</p>
        )}
      </div>
    );
  }
  