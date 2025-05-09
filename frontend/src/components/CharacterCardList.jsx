import CharacterCard from "./CharacterCard";

export default function CharacterCardList({ data }) {
  const pageToSources = {};
  if (data.sources) {
    for (const src of data.sources) {
      const page = src.page;
      if (!pageToSources[page]) pageToSources[page] = [];
      pageToSources[page].push(src);
    }
  }

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
        {data.cards.map((char, idx) => {
          const relatedSources = pageToSources[char.page] || [];
          return (
            <CharacterCard key={idx} character={{ ...char, sources: relatedSources }} />
          );
        })}
      </div>
    </div>
  );
}
