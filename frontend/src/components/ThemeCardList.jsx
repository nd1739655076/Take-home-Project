import ThemeCard from "./ThemeCard";

export default function ThemeCardList({ data }) {
  return (
    <div className="px-6 py-10 max-w-6xl mx-auto space-y-10">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-green-800 mb-2">{data.title}</h1>
      </div>

      <div className="space-y-6">
        {data.themes.map((theme, idx) => (
          <ThemeCard key={idx} theme={theme} />
        ))}
      </div>
    </div>
  );
}
