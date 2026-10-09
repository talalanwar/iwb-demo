import { useState } from 'react';
// Using emoji icon

interface ReviewNoteFormProps {
  onSubmit: (reviewerName: string, noteText: string) => Promise<void>;
}

export default function ReviewNoteForm({ onSubmit }: ReviewNoteFormProps) {
  const [reviewerName, setReviewerName] = useState('');
  const [noteText, setNoteText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!reviewerName.trim() || !noteText.trim()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(reviewerName.trim(), noteText.trim());
      setNoteText(''); // Clear note text after successful submission, keep name
    } catch (err) {
      console.error('Failed to submit review note:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-6">
      <div className="mb-4">
        <label htmlFor="reviewerName" className="block text-sm font-semibold text-gray-800 mb-2">
          Your Name
        </label>
        <input
          type="text"
          id="reviewerName"
          value={reviewerName}
          onChange={(e) => setReviewerName(e.target.value)}
          placeholder="Enter your name"
          required
          className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
        />
      </div>

      <label htmlFor="reviewNote" className="block text-sm font-semibold text-gray-800 mb-2">
        Add Review Note
      </label>
      <textarea
        id="reviewNote"
        value={noteText}
        onChange={(e) => setNoteText(e.target.value)}
        placeholder="Enter your review feedback or suggestions..."
        required
        className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[100px] leading-relaxed"
      />
      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-flex items-center gap-2 px-6 py-3 mt-3 text-base font-semibold text-white rounded-lg transition-all hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)] active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed"
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}
      >
        <span>{isSubmitting ? 'Submitting...' : '📤 Submit Review Note'}</span>
      </button>
    </form>
  );
}
