// Using text icons

interface ReviewWorkspaceSnapshotProps {
  workspace: {
    product_name: string;
    vision_statement: string;
    target_problem: string;
    business_goals_json: string[];
  };
  stories: Array<{
    id: number;
    title: string;
    actor: string;
    need_text: string;
    outcome_text: string;
    priority: string | null;
    acceptance_criteria: Array<{ criterion_text: string }>;
  }>;
  readinessSummary: {
    story_count: number;
    stories_with_criteria: number;
    stories_prioritized: number;
    readiness_percentage: number;
  };
}

export default function ReviewWorkspaceSnapshot({
  workspace,
  stories,
  readinessSummary
}: ReviewWorkspaceSnapshotProps) {
  return (
    <div className="space-y-6">
      {/* Vision & Business Context */}
      <div className="bg-white rounded-xl px-8 py-8 border border-gray-300">
        <div className="flex items-center gap-3 mb-5 pb-4 border-b border-gray-300">
          <div className="w-9 h-9 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center">
            <span className="text-lg">💡</span>
          </div>
          <h2 className="text-xl font-bold text-gray-900">Vision & Business Context</h2>
        </div>

        <div className="space-y-5">
          <div>
            <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
              Vision Statement
            </div>
            <div className="text-base text-gray-800 leading-relaxed">{workspace.vision_statement}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
              Target Problem
            </div>
            <div className="text-base text-gray-800 leading-relaxed">{workspace.target_problem}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
              Business Goals
            </div>
            <div className="text-base text-gray-800 leading-relaxed">
              {workspace.business_goals_json.join('. ')}
            </div>
          </div>
        </div>
      </div>

      {/* User Stories & Backlog */}
      <div className="bg-white rounded-xl px-8 py-8 border border-gray-300">
        <div className="flex items-center gap-3 mb-5 pb-4 border-b border-gray-300">
          <div className="w-9 h-9 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center">
            <span className="text-lg">📋</span>
          </div>
          <h2 className="text-xl font-bold text-gray-900">User Stories & Backlog</h2>
        </div>

        <div className="space-y-4">
          {stories.map((story) => (
            <div key={story.id} className="bg-gray-50 rounded-lg px-5 py-5">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 mb-1.5">{story.title}</h3>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    As a {story.actor}, I want {story.need_text} so that {story.outcome_text}
                  </p>
                </div>
                <div
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold flex-shrink-0 ml-3 ${
                    story.priority === 'HIGH'
                      ? 'bg-red-100 text-red-800'
                      : story.priority === 'MEDIUM'
                      ? 'bg-orange-100 text-orange-800'
                      : 'bg-blue-100 text-blue-800'
                  }`}
                >
                  <span>{story.priority === 'HIGH' ? '↑ High' : story.priority === 'MEDIUM' ? '− Medium' : '○ Low'}</span>
                </div>
              </div>

              {story.acceptance_criteria && story.acceptance_criteria.length > 0 && (
                <ul className="space-y-1.5 mt-3">
                  {story.acceptance_criteria.map((criterion, index) => (
                    <li key={index} className="flex items-start gap-2 text-xs text-gray-700 leading-relaxed">
                      <span className="text-green-600 flex-shrink-0">✓</span>
                      <span>{criterion.criterion_text}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Readiness Status */}
      <div className="bg-white rounded-xl px-8 py-8 border border-gray-300">
        <div className="flex items-center gap-3 mb-5 pb-4 border-b border-gray-300">
          <div className="w-9 h-9 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center">
            <span className="text-lg">✓</span>
          </div>
          <h2 className="text-xl font-bold text-gray-900">Readiness Status</h2>
        </div>

        <div className="grid grid-cols-4 gap-4">
          <div className="bg-gray-50 rounded-lg px-4 py-4 text-center">
            <div className="text-3xl font-bold text-gray-900">{readinessSummary.story_count}</div>
            <div className="text-xs text-gray-500 uppercase tracking-wide">Total Stories</div>
          </div>
          <div className="bg-gray-50 rounded-lg px-4 py-4 text-center">
            <div className="text-3xl font-bold text-gray-900">{readinessSummary.stories_with_criteria}</div>
            <div className="text-xs text-gray-500 uppercase tracking-wide">With Criteria</div>
          </div>
          <div className="bg-gray-50 rounded-lg px-4 py-4 text-center">
            <div className="text-3xl font-bold text-gray-900">{readinessSummary.stories_prioritized}</div>
            <div className="text-xs text-gray-500 uppercase tracking-wide">Prioritized</div>
          </div>
          <div className="bg-gray-50 rounded-lg px-4 py-4 text-center">
            <div className="text-3xl font-bold text-gray-900">{readinessSummary.readiness_percentage}%</div>
            <div className="text-xs text-gray-500 uppercase tracking-wide">Ready</div>
          </div>
        </div>
      </div>
    </div>
  );
}
