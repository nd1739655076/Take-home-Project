// src/components/LayoutRenderer.jsx
import SymbolList from "./SymbolList";

export default function LayoutRenderer({ layout, data }) {
  switch (layout) {
    case "symbol_list":
      return <SymbolList data={data.symbols} />;
    default:
      return <p className="text-red-500">Unsupported layout: {layout}</p>;
  }
}
