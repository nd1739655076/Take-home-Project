export default function CharacterCard({ character }) {
  return (
    <div className="bg-blue-100 rounded-xl p-6 shadow-md flex flex-col min-h-[320px]">
      <div>
        <h2 className="text-xl font-bold text-blue-900 mb-2">{character.name}</h2>
        <p className="text-sm text-blue-900 mb-3">{character.description}</p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-3">
          {character.personality_traits.map((trait, idx) => (
            <span
              key={idx}
              className="text-xs bg-white px-2 py-1 rounded-full shadow-sm text-blue-700 border"
            >
              {trait}
            </span>
          ))}
        </div>

        {/* Key Actions */}
        {character.key_actions && character.key_actions.length > 0 && (
          <div className="mb-3 text-sm">
            <h3 className="font-semibold text-blue-800 mb-1">Key Actions:</h3>
            <ul className="list-disc list-inside text-blue-900 space-y-1">
              {character.key_actions.map((action, idx) => (
                <li key={idx}>{action}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
