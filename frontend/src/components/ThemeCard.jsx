export default function ThemeCard({ theme }) {
  return (
    <div className="bg-green-50 rounded-xl p-6 shadow space-y-4">
      <h2 className="text-xl font-bold text-green-900">{theme.name}</h2>
      <p className="text-sm text-gray-800">{theme.description}</p>

      <div>
        <h3 className="text-sm font-semibold text-green-700">Key Quotes:</h3>
        <ul className="list-disc pl-6 text-sm text-gray-700">
          {theme.examples.map((ex, idx) => (
            <li key={idx} className="mb-1">
              “{ex.quote}” <span className="text-xs text-green-600">— Page {ex.page}</span>
            </li>
          ))}
        </ul>
      </div>

      {theme.related_characters?.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-green-700">Related Characters:</h3>
          <div className="flex flex-wrap gap-2 mt-1">
            {theme.related_characters.map((char, idx) => (
              <span key={idx} className="text-xs bg-white px-2 py-1 rounded-full border text-green-800">
                {char}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
