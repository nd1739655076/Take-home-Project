// src/components/SymbolList.jsx

import { useState } from "react";
import SymbolDetail from "./SymbolDetail";

export default function SymbolList({ data }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const selectedSymbol = data[selectedIndex];

  return (
    <div className="px-4 py-8 max-w-5xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-4">
        Important Symbols in The Great Gatsby
      </h1>

      {/* Tab selector */}
      <div className="flex flex-wrap justify-center gap-3 mb-4">
        {data.map((symbol, idx) => (
          <button
            key={idx}
            onClick={() => setSelectedIndex(idx)}
            className={`px-4 py-2 rounded-full text-sm font-medium border transition ${
              selectedIndex === idx
                ? "bg-blue-600 text-white"
                : "bg-white text-blue-600 border-blue-600"
            }`}
          >
            {symbol.name}
          </button>
        ))}
      </div>

      {/* Detail view */}
      <SymbolDetail symbol={selectedSymbol} />
    </div>
  );
}
