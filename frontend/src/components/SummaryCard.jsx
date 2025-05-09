export default function SummaryCard({ point }) {
    return (
      <div className="bg-purple-100 rounded-xl p-4 shadow-sm text-sm text-gray-800 hover:shadow-md transition">
        {point}
      </div>
    );
  }