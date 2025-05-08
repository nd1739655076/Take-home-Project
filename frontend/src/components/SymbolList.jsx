// src/components/SymbolList.jsx
import SymbolCard from "./SymbolCard";

export default function SymbolList({ data }) {
  return (
    <div className="px-6 py-10 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6"> Symbol Analysis</h1>
      {data.map((symbol, index) => (
        <SymbolCard key={index} symbol={symbol} />
      ))}
    </div>
  );
}
