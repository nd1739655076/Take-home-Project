// src/components/CharacterCard.jsx

export default function CharacterCard({ character }) {
    return (
      <div className="bg-blue-100 rounded-xl p-6 shadow-md flex flex-col justify-between min-h-[320px]">
        <div>
          <h2 className="text-xl font-bold text-blue-900 mb-2">{character.name}</h2>
          <p className="text-sm text-blue-900 mb-3">{character.description}</p>
  
          {/* Tags */}
          <div className="flex flex-wrap gap-2 mb-3">
            {character.personality_traits.map((trait, idx) => (
              <span key={idx} className="text-xs bg-white px-2 py-1 rounded-full shadow-sm text-blue-700 border">
                {trait}
              </span>
            ))}
          </div>
  
          {/* Quote */}
          <p className="text-sm italic text-blue-800 mb-1">
            “{character.quote}”
          </p>
          {character.page && (
            <p className="text-xs text-blue-500 mb-3">— Page {character.page}</p>
          )}
        </div>
  
        {/* Button */}
        <button className="mt-auto bg-white text-blue-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-200 transition">
            Read more on page {character.page}
        </button>
      </div>
    );
  }
  