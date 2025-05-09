export default function ContextParagraphCard({ data }) {
  return (
    <div className="px-6 py-10 max-w-5xl mx-auto space-y-8">
      {/* Title */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-800">{data.title || "Answer"}</h1>
        <p className="text-sm text-gray-600 mt-1">Generated explanation with supporting quotes</p>
      </div>

      {/* Main context flashcard */}
      {data.context && (
        <div className="bg-white rounded-xl shadow p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-blue-700 mb-2">Summary</h2>
          <p className="text-sm text-gray-800">{data.context}</p>
        </div>
      )}

      {/* GPT-selected quotes */}
      {data.quotes?.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {data.quotes.map((q, idx) => (
            <div
              key={idx}
              className="bg-blue-50 rounded-xl shadow-sm p-5 border border-blue-100"
            >
              <p className="italic text-blue-800 text-sm">“{q.quote}”</p>
              {q.page && (
                <p className="text-xs text-blue-500 mt-2">— Page {q.page}</p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Source chunks */}
      {data.sources?.length > 0 && (
        <div className="mt-8 text-sm text-gray-700 bg-gray-50 border rounded-xl p-6">
          <h2 className="font-medium text-gray-800 mb-3">📖 Source Snippets</h2>
          <ul className="list-disc list-inside space-y-1">
            {data.sources.map((s, idx) => (
              <li key={idx}>
                <strong>Page {s.page}:</strong> {s.content}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
