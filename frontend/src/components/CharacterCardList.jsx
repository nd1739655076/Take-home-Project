// src/components/CharacterCardList.jsx

import CharacterCard from "./CharacterCard";

export default function CharacterCardList({ data }) {
    return (
      <div className="px-6 py-10 max-w-6xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-blue-800 mb-2">{data.title}</h1>
          {data.intro && (
            <p className="text-sm text-gray-600 max-w-2xl mx-auto">{data.intro}</p>
          )}
        </div>
  
        {/* Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {data.cards.map((char, idx) => (
            <CharacterCard key={idx} character={char} />
          ))}
        </div>
  
        {/* Optional context paragraph if provided */}
        {data.context && (
          <div className="bg-white rounded-xl p-6 shadow text-sm text-gray-800 max-w-3xl mx-auto">
            <h2 className="text-md font-semibold text-blue-700 mb-2">{data.context.title || "Context"}</h2>
            <p>{data.context.body}</p>
          </div>
        )}
      </div>
    );
  }
  
