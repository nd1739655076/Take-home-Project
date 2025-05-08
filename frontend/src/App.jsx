import LayoutRenderer from "./components/LayoutRenderer";
import mockResponse from "./mockSymbolData.json";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <LayoutRenderer layout={mockResponse.layout} data={mockResponse} />
    </div>
  );
}

export default App;