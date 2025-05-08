export default function QuoteAnalysis({ data }) {
    return (
      <div className="bg-white rounded-xl shadow p-6 max-w-3xl mx-auto">
        <h2 className="text-xl font-semibold text-blue-800 mb-2">Quote Analysis</h2>
  
        <blockquote className="border-l-4 border-blue-400 pl-4 italic text-gray-800 mb-3">
          “{data.quote}”
        </blockquote>
  
        <p className="text-sm text-gray-600 mb-1">
          <strong>Speaker:</strong> {data.speaker}
        </p>
        <p className="text-sm text-gray-600 mb-1">
          <strong>Chapter:</strong> {data.chapter} | <strong>Page:</strong> {data.page}
        </p>
  
        <div className="mt-4">
          <h3 className="font-medium text-gray-800 mb-1">Interpretation:</h3>
          <p className="text-sm text-gray-700">{data.interpretation}</p>
        </div>
  
        <div className="mt-4">
          <h3 className="font-medium text-gray-800 mb-1">Significance:</h3>
          <p className="text-sm text-gray-700">{data.significance}</p>
        </div>
  
        <div className="mt-4">
          <h3 className="font-medium text-gray-800 mb-1">Themes:</h3>
          <div className="flex flex-wrap gap-2 mt-1">
            {data.themes.map((theme, idx) => (
              <span key={idx} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                {theme}
              </span>
            ))}
          </div>
        </div>
      </div>
    );
  }
  