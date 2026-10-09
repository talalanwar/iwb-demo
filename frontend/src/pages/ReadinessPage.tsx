import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
// Using emoji icons instead of lucide-react
import { AppShell } from '../components/common/AppShell';
import ReadinessSummaryCard from '../components/readiness/ReadinessSummaryCard';
import GapList from '../components/readiness/GapList';
import { getReadiness } from '../api/workspaceApi';
import type { ReadinessResponse } from '../types/readiness';

export default function ReadinessPage() {
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadReadiness();
  }, []);

  const loadReadiness = async () => {
    try {
      const data = await getReadiness();
      setReadiness(data);
    } catch (err) {
      setError('Failed to load readiness summary');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (status: string) => {
    switch (status) {
      case 'READY_FOR_REVIEW':
        return { bg: 'rgba(72, 187, 120, 0.2)', border: '#48bb78', text: '#2f855a' };
      case 'IN_PROGRESS':
        return { bg: 'rgba(237, 137, 54, 0.2)', border: '#ed8936', text: '#dd6b20' };
      case 'NEEDS_ATTENTION':
        return { bg: 'rgba(237, 137, 54, 0.2)', border: '#ed8936', text: '#dd6b20' };
      default:
        return { bg: 'rgba(160, 174, 192, 0.2)', border: '#a0aec0', text: '#718096' };
    }
  };

  const mapGapsToComponent = (gaps: any[]) => {
    return gaps.map(gap => ({
      code: gap.code,
      title: gap.code.replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase()),
      description: gap.message,
      navigate_to: gap.navigate_to || '/backlog'
    }));
  };

  const getStatusMessage = (status: string, gapCount: number) => {
    switch (status) {
      case 'READY_FOR_REVIEW':
        return 'Ready for Review';
      case 'IN_PROGRESS':
        return 'In Progress';
      case 'NEEDS_ATTENTION':
        return 'Almost Ready for Review';
      default:
        return 'Not Started';
    }
  };

  if (isLoading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-600">Loading readiness summary...</div>
        </div>
      </AppShell>
    );
  }

  if (error || !readiness) {
    return (
      <AppShell>
        <div className="max-w-6xl mx-auto px-8 py-10">
          <div className="bg-red-50 border border-red-300 rounded-lg px-4 py-3">
            <p className="text-red-700 text-sm font-medium">{error || 'Failed to load readiness'}</p>
          </div>
        </div>
      </AppShell>
    );
  }

  const scoreColor = getScoreColor(readiness.status);
  const readinessPercentage = (readiness.summary as any).readiness_percentage || 0;
  const gapCount = readiness.gaps?.length || 0;
  const mappedGaps = mapGapsToComponent(readiness.gaps || []);

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto px-8 py-10">
        <div className="mb-8">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
            <Link to="/" className="text-purple-600 hover:underline">
              Dashboard
            </Link>
            <span>&gt;</span>
            <span>Readiness Summary</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Readiness Summary</h1>
          <p className="text-lg text-gray-600">
            Review completeness indicators and fix any gaps before sharing your workspace
          </p>
        </div>

        {/* Readiness Score Circle */}
        <div className="bg-white rounded-2xl px-8 py-8 border border-gray-300 mb-8 text-center">
          <div
            className="w-30 h-30 mx-auto mb-6 rounded-full flex items-center justify-center flex-col"
            style={{
              width: '120px',
              height: '120px',
              background: `linear-gradient(135deg, ${scoreColor.bg} 0%, ${scoreColor.bg} 100%)`,
              border: `8px solid ${scoreColor.border}`
            }}
          >
            <span className="text-4xl font-bold" style={{ color: scoreColor.text }}>
              {readinessPercentage}%
            </span>
            <span className="text-xs uppercase tracking-wide" style={{ color: '#a0aec0' }}>
              Ready
            </span>
          </div>
          <div className="text-xl font-bold text-gray-900 mb-2">
            {getStatusMessage(readiness.status, gapCount)}
          </div>
          <p className="text-base text-gray-600">
            {gapCount > 0 
              ? `Fix ${gapCount} ${gapCount === 1 ? 'gap' : 'gaps'} to complete your product definition`
              : 'Your workspace is ready for review!'}
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <ReadinessSummaryCard
            title="Vision & Context"
            status={(readiness.summary as any).vision_complete ? 'complete' : 'incomplete'}
            description="Product vision, target problem, business goals, and success measures are defined."
          />
          <ReadinessSummaryCard
            title="User Stories"
            status={(readiness.summary as any).all_stories_have_criteria ? 'complete' : 'incomplete'}
            stats={[
              { value: (readiness.summary as any).story_count, label: 'Total Stories' },
              { value: (readiness.summary as any).stories_with_criteria, label: 'With Criteria' }
            ]}
          />
          <ReadinessSummaryCard
            title="Prioritization"
            status={(readiness.summary as any).all_stories_prioritized ? 'complete' : 'incomplete'}
            stats={[
              { value: (readiness.summary as any).stories_prioritized, label: 'Prioritized' },
              { value: (readiness.summary as any).story_count - (readiness.summary as any).stories_prioritized, label: 'Unprioritized' }
            ]}
          />
        </div>

        {/* Gaps Section */}
        {gapCount > 0 && (
          <div className="bg-white rounded-xl px-8 py-8 border border-gray-300 mb-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-orange-100 text-orange-800 flex items-center justify-center">
                <span className="text-xl">⚠️</span>
              </div>
              <h2 className="text-xl font-bold text-gray-900">Gaps Found ({gapCount})</h2>
            </div>
            <GapList gaps={mappedGaps} />
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            disabled={gapCount > 0}
            className={`inline-flex items-center gap-2 px-7 py-3.5 text-lg font-semibold text-white rounded-lg transition-all ${
              gapCount > 0
                ? 'opacity-50 cursor-not-allowed'
                : 'hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)] active:translate-y-0'
            }`}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}
          >
            <span>🔗 Share for Review</span>
          </button>
          <Link
            to="/backlog"
            className="inline-flex items-center gap-2 px-7 py-3.5 text-lg font-semibold text-purple-600 bg-white border-2 border-purple-600 rounded-lg transition-all hover:bg-purple-50"
          >
            <span>← Back to Backlog</span>
          </Link>
        </div>
      </div>
    </AppShell>
  );
}
