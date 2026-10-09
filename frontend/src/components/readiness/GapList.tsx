import { Link } from 'react-router-dom';

interface GapItem {
  code: string;
  title: string;
  description: string;
  navigate_to: string;
}

interface GapListProps {
  gaps: GapItem[];
}

export default function GapList({ gaps }: GapListProps) {
  const getIcon = (code: string) => {
    if (code === 'MISSING_ACCEPTANCE_CRITERIA') {
      return <span className="text-xl">☐</span>;
    }
    return <span className="text-xl">📋</span>;
  };

  if (gaps.length === 0) {
    return (
      <div className="text-center py-8 text-gray-600">
        No gaps found. Your workspace is ready for review!
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {gaps.map((gap, index) => (
        <div
          key={index}
          className="bg-yellow-50 border border-yellow-300 rounded-lg px-4 py-4 flex items-start gap-4"
        >
          <div className="w-10 h-10 rounded-lg bg-orange-200 text-orange-800 flex items-center justify-center flex-shrink-0">
            {getIcon(gap.code)}
          </div>
          <div className="flex-1">
            <div className="text-base font-semibold text-gray-900 mb-1">{gap.title}</div>
            <p className="text-sm text-gray-600 mb-3">{gap.description}</p>
            <Link
              to={gap.navigate_to}
              className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-purple-600 bg-white border border-purple-600 rounded-md transition-all hover:bg-purple-50"
            >
              <span>Fix in Backlog →</span>
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
}
