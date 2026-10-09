// Using text symbols instead of lucide-react icons

interface StoryCardProps {
  story: {
    id: number;
    title: string;
    actor: string;
    need_text: string;
    outcome_text: string;
    priority: string | null;
    acceptance_criteria: Array<{ id: number; criterion_text: string }>;
  };
  onEdit: (story: any) => void;
  onDelete: (storyId: number) => void;
}

export default function StoryCard({ story, onEdit, onDelete }: StoryCardProps) {
  const description = `As a ${story.actor}, I want ${story.need_text} so that ${story.outcome_text}`;
  const hasCriteria = story.acceptance_criteria && story.acceptance_criteria.length > 0;

  const getPriorityBadge = () => {
    switch (story.priority) {
      case 'HIGH':
        return (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-red-100 text-red-800">
            <span>↑ High Priority</span>
          </div>
        );
      case 'MEDIUM':
        return (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-orange-100 text-orange-800">
            <span>− Medium Priority</span>
          </div>
        );
      case 'LOW':
        return (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
            <span>○ Low Priority</span>
          </div>
        );
      default:
        return (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-gray-100 text-gray-600">
            <span>○ Not Prioritized</span>
          </div>
        );
    }
  };

  return (
    <div className="bg-white rounded-xl px-6 py-6 border border-gray-300 transition-all hover:shadow-[0_4px_12px_rgba(0,0,0,0.08)] hover:border-gray-400">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900 mb-2">{story.title}</h3>
          <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
        </div>
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onEdit(story)}
            className="w-9 h-9 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 transition-all hover:bg-gray-50 hover:border-gray-400 hover:text-gray-800"
            title="Edit story"
          >
            <span>✏️</span>
          </button>
          <button
            onClick={() => onDelete(story.id)}
            className="w-9 h-9 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 transition-all hover:bg-gray-50 hover:border-gray-400 hover:text-gray-800"
            title="Delete story"
          >
            <span>🗑️</span>
          </button>
        </div>
      </div>

      <div className="flex items-center gap-4 mb-4">
        {getPriorityBadge()}
        <div className="flex items-center gap-1.5 text-xs" style={{ color: hasCriteria ? '#718096' : '#dd6b20' }}>
          <span style={{ fontWeight: hasCriteria ? 400 : 600 }}>
            {hasCriteria 
              ? `☑ ${story.acceptance_criteria.length} acceptance ${story.acceptance_criteria.length === 1 ? 'criterion' : 'criteria'}`
              : '☐ No acceptance criteria'}
          </span>
        </div>
      </div>

      {hasCriteria && (
        <div className="bg-gray-50 rounded-lg px-4 py-4">
          <div className="text-xs font-semibold text-gray-800 uppercase tracking-wide mb-3">
            Acceptance Criteria
          </div>
          <ul className="space-y-2">
            {story.acceptance_criteria.map((criterion) => (
              <li key={criterion.id} className="flex items-start gap-2 text-sm text-gray-700 leading-relaxed">
                <span className="text-green-600 flex-shrink-0">✓</span>
                <span>{criterion.criterion_text}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
