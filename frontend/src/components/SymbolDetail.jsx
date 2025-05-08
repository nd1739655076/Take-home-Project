// src/components/SymbolDetail.jsx

export default function SymbolDetail({ symbol }) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6 space-y-6">
  
        {/* Description and Analysis */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-1">Description</h3>
            <p className="text-gray-700">{symbol.description}</p>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-1">Analysis</h3>
            <p className="text-gray-700">{symbol.meaning}</p>
          </div>
        </div>

        {/* key quote */}
  
        <div className="bg-purple-100 rounded-lg p-4 text-center">
          <p className="italic text-blue-900 font-medium">
            “{symbol.key_quote}”
            {symbol.page && <span className="text-sm text-gray-500 ml-2">(Page {symbol.page})</span>}
          </p>
        </div>

        {/* Reference list */}
        <div>
          <h4 className="text-md font-semibold text-gray-800 mb-2">Page References</h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {symbol.references.map((ref, idx) => (
              <div key={idx} className="border rounded-md p-3 text-sm bg-gray-50 shadow-sm">
                <p>{ref.description}</p>
                <p className="text-blue-600 text-xs mt-1">Go to page {ref.page}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
  