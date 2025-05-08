// src/components/SymbolCard.jsx


export default function SymbolCard({ symbol }) {
    return (
        <div className="bg-white shadow-md rounded-xl p-6 mb-6">
            <h2 className="text-2xl font-bold text-blue-700 mb-2"> {symbol.name} </h2>
            <p className="text-gray-700 mb-2">
                <span className="font-semibold">Description: </span>{symbol.description}
            </p>

            <p className="text-gray-700 mb-2">
                <span className="font-semibold">Meaning: </span>{symbol.meaning}
            </p>

            <p className="italic text-gray-600 mb-2">
                <span className="font-semibold">Key Quote: </span>“{symbol.key_quote}”
                {symbol.page && <span className="text-sm text-gray-500 ml-2"> (Page {symbol.page})</span>}
            </p>
            <div className="mt-3">
                <h3 className="text-md font-semibold text-gray-800 mb-1">📘 References:</h3>
                <ul className="list-disc pl-5 text-gray-700 text-sm space-y-1">
                    {symbol.references.map((ref, idx) => (
                        <li key={idx}>
                            {ref.description} <span className="text-gray-500">(Page {ref.page})</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}