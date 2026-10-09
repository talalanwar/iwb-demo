import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
// Using emoji icons
import ReviewWorkspaceSnapshot from '../components/review/ReviewWorkspaceSnapshot';
import ReviewNoteForm from '../components/review/ReviewNoteForm';
import { getReviewSnapshot, createReviewNote } from '../api/reviewApi';
import type { ReviewSnapshotResponse } from '../types/review';

export default function ReviewPage() {
  const { shareToken } = useParams<{ shareToken: string }>();
  const [review, setReview] = useState<ReviewSnapshotResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (shareToken) {
      loadReview(shareToken);
    }
  }, [shareToken]);

  const loadReview = async (token: string) => {
    try {
      const data = await getReviewSnapshot(token);
      setReview(data);
    } catch (err) {
      setError('Failed to load review workspace');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitNote = async (reviewerName: string, noteText: string) => {
    if (!shareToken) return;
    
    await createReviewNote(shareToken, {
      reviewerName,
      noteText
    });
    
    // Reload to show new note
    await loadReview(shareToken);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white border-b border-gray-300 px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-lg" style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}>
              PLS
            </div>
            <span className="text-lg font-bold text-gray-900">Product Learning Studio</span>
            <span className="px-3 py-1.5 bg-purple-100 text-purple-600 text-xs font-semibold rounded-md">
              Review Mode
            </span>
          </div>
        </nav>
        <div className="flex items-center justify-center min-h-[calc(100vh-73px)]">
          <div className="text-gray-600">Loading review...</div>
        </div>
      </div>
    );
  }

  if (error || !review) {
    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white border-b border-gray-300 px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-lg" style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}>
              PLS
            </div>
            <span className="text-lg font-bold text-gray-900">Product Learning Studio</span>
          </div>
        </nav>
        <div className="max-w-5xl mx-auto px-8 py-10">
          <div className="bg-red-50 border border-red-300 rounded-lg px-4 py-3">
            <p className="text-red-700 text-sm font-medium">{error || 'Failed to load review'}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-300 px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-lg" style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
          }}>
            PLS
          </div>
          <span className="text-lg font-bold text-gray-900">Product Learning Studio</span>
          <span className="px-3 py-1.5 bg-purple-100 text-purple-600 text-xs font-semibold rounded-md">
            Review Mode
          </span>
        </div>
        <div className="flex items-center gap-4">
          <button className="px-5 py-2.5 text-sm font-semibold text-gray-600 bg-white border border-gray-300 rounded-md transition-all hover:bg-gray-50 hover:border-gray-400">
            Close Review
          </button>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-8 py-10">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Review: {(review.workspace as any).product_name}
          </h1>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <div className="flex items-center gap-1.5">
              <span>👤</span>
              <span>Created by Product Learner</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span>📅</span>
              <span>Last updated: {formatDate((review.workspace as any).updated_at)}</span>
            </div>
          </div>
        </div>

        <ReviewWorkspaceSnapshot
          workspace={(review as any).workspace}
          stories={(review as any).stories}
          readinessSummary={(review as any).readiness_summary}
        />

        <div className="bg-white rounded-xl px-8 py-8 border border-gray-300 mt-6">
          <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-300">
            <div className="w-9 h-9 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center">
              <span className="text-xl">💬</span>
            </div>
            <h2 className="text-xl font-bold text-gray-900">Review Notes</h2>
          </div>

          {(review as any).review_notes && (review as any).review_notes.length > 0 && (
            <div className="space-y-4 mb-6">
              {(review as any).review_notes.map((note: any) => (
                <div key={note.id} className="bg-yellow-50 border border-yellow-300 rounded-lg px-4 py-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-900">{note.reviewer_name}</span>
                    <span className="text-xs text-gray-500">{formatDate(note.created_at)}</span>
                  </div>
                  <p className="text-sm text-gray-700 leading-relaxed">{note.note_text}</p>
                </div>
              ))}
            </div>
          )}

          <ReviewNoteForm onSubmit={handleSubmitNote} />
        </div>
      </div>
    </div>
  );
}
