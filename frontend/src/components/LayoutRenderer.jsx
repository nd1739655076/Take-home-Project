// src/components/LayoutRenderer.jsx
import CharacterCardList from "./CharacterCardList";
import SymbolList from "./SymbolList";
import TimelineLayout from "./TimelineLayout";
import QuoteAnalysis from "./QuoteAnalysis";

export default function LayoutRenderer({ layout, data }) {
  switch (layout) {
    case "symbol_list":
      return <SymbolList data={data.symbols} />;
    case "character_cards":
      return <CharacterCardList data={data} />;
    case "timeline":
      return <TimelineLayout data={data} />
    case "quote_analysis":
      return <QuoteAnalysis data={data} />
    default:
      return <p className="text-red-500">Unsupported layout: {layout}</p>;
  }
}
