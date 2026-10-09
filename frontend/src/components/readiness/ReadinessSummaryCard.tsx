// Using text icons

interface ReadinessSummaryCardProps {
  title: string;
  status: 'complete' | 'incomplete';
  description?: string;
  stats?: Array<{ value: string | number; label: string }>;
}

export default function ReadinessSummaryCard({
  title,
  status,
  description,
  stats
}: ReadinessSummaryCardProps) {
  return (
    <div className="bg-white rounded-xl px-6 py-6 border border-gray-300">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-900">{title}</h3>
        <div
          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${
            status === 'complete'
              ? 'bg-green-100 text-green-800'
              : 'bg-orange-100 text-orange-800'
          }`}
        >
          <span>{status === 'complete' ? '✓ Complete' : '⚠ Incomplete'}</span>
        </div>
      </div>

      {description && (
        <p className="text-sm text-gray-600 mb-4">{description}</p>
      )}

      {stats && stats.length > 0 && (
        <div className="flex gap-6">
          {stats.map((stat, index) => (
            <div key={index} className="flex flex-col">
              <span className="text-3xl font-bold text-gray-900">{stat.value}</span>
              <span className="text-xs text-gray-500 uppercase tracking-wide">{stat.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
