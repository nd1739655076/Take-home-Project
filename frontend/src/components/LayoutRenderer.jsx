// src/components/LayoutRenderer.jsx
import CharacterCardList from "./CharacterCardList";
import SymbolList from "./SymbolList";
import TimelineLayout from "./TimelineLayout";
import QuoteAnalysis from "./QuoteAnalysis";
import SummaryCardList from "./SummaryCardList";
import ContextParagraphCard from "./ContextParagraphCard";
import ThemeCardList from "./ThemeCardList";

export default function LayoutRenderer({ layout, data }) {
  switch (layout) {
    case "symbol_list":
      return <SymbolList data={data.symbols} />;
    case "character_cards":
      return <CharacterCardList data={data} />;
    case "timeline":
      return <TimelineLayout data={data} />;
    case "quote_analysis":
      return <QuoteAnalysis data={data} />;
    case "summary":
      return <SummaryCardList data={data} />;
    case "theme":
      return <ThemeCardList data={data} />
    default:
      return <ContextParagraphCard data={data} />;
  }
}
