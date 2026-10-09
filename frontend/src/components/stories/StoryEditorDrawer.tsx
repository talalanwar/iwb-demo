import { useState, useEffect } from 'react';
// Using emoji icons

interface StoryEditorDrawerProps {
  story: {
    id?: number;
    title: string;
    actor: string;
    need_text: string;
    outcome_text: string;
    priority: string | null;
    acceptance_criteria: Array<{ id?: number; criterion_text: string }>;
  } | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (story: any) => void;
}

export default function StoryEditorDrawer({ story, isOpen, onClose, onSave }: StoryEditorDrawerProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('');
  const [criteria, setCriteria] = useState<string[]>([]);
  const [validationError, setValidationError] = useState('');

  useEffect(() => {
    if (story) {
      setTitle(story.title || '');
      setDescription(`As a ${story.actor}, I want ${story.need_text} so that ${story.outcome_text}` || '');
      setPriority(story.priority || '');
      setCriteria(story.acceptance_criteria?.map(c => c.criterion_text) || ['']);
    } else {
      setTitle('');
      setDescription('');
      setPriority('');
      setCriteria(['']);
    }
    setValidationError('');
  }, [story]);

  const handleAddCriterion = () => {
    setCriteria([...criteria, '']);
  };

  const handleRemoveCriterion = (index: number) => {
    setCriteria(criteria.filter((_, i) => i !== index));
  };

  const handleCriterionChange = (index: number, value: string) => {
    const newCriteria = [...criteria];
    newCriteria[index] = value;
    setCriteria(newCriteria);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const validCriteria = criteria.filter(c => c.trim());
    if (validCriteria.length === 0) {
      setValidationError('Please add at least one acceptance criterion before saving.');
      return;
    }

    // Parse description to extract actor, need, outcome
    const match = description.match(/^As an? (.+?), I want (.+?) so that (.+?)\.?$/i);
    if (!match) {
      setValidationError('Story description must follow format: As a [user], I want [goal], so that [benefit]');
      return;
    }

    const [, actor, need, outcome] = match;

    onSave({
      id: story?.id,
      title: title.trim(),
      actor: actor.trim(),
      need_text: need.trim(),
      outcome_text: outcome.trim(),
      priority: priority || null,
      acceptance_criteria: validCriteria.map((text, index) => ({
        id: story?.acceptance_criteria?.[index]?.id,
        criterion_text: text.trim()
      }))
    });
    
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
      <div className="min-h-screen px-5 py-10 flex items-start justify-center">
        <div className="bg-white rounded-2xl w-full max-w-3xl shadow-[0_20px_60px_rgba(0,0,0,0.3)]">
          <div className="px-8 py-8 border-b border-gray-300">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {story?.id ? 'Edit User Story' : 'Add New Story'}
            </h2>
            <p className="text-sm text-gray-600">
              {story?.id ? 'Update the story details and acceptance criteria' : 'Create a new user story with acceptance criteria'}
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="px-8 py-8">
              {validationError && (
                <div className="flex items-center gap-3 bg-red-50 border border-red-300 rounded-lg px-4 py-3 mb-6">
                  <span className="text-red-700 text-xl">⚠️</span>
                  <span className="text-red-700 text-sm font-medium">{validationError}</span>
                </div>
              )}

              <div className="mb-6">
                <label htmlFor="storyTitle" className="block text-sm font-semibold text-gray-800 mb-2">
                  Story Title <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  id="storyTitle"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Brief, descriptive title for the story"
                  required
                  className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
                />
              </div>

              <div className="mb-6">
                <label htmlFor="storyDescription" className="block text-sm font-semibold text-gray-800 mb-2">
                  Story Description <span className="text-red-600">*</span>
                </label>
                <textarea
                  id="storyDescription"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="As a [user], I want [goal], so that [benefit]"
                  required
                  className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[100px] leading-relaxed"
                />
                <p className="mt-1.5 text-xs text-gray-500">Use the standard user story format to describe the need and benefit</p>
              </div>

              <div className="mb-6">
                <label htmlFor="priority" className="block text-sm font-semibold text-gray-800 mb-2">
                  Priority <span className="text-red-600">*</span>
                </label>
                <select
                  id="priority"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  required
                  className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
                >
                  <option value="">Select priority level</option>
                  <option value="HIGH">High Priority</option>
                  <option value="MEDIUM">Medium Priority</option>
                  <option value="LOW">Low Priority</option>
                </select>
                <p className="mt-1.5 text-xs text-gray-500">Assign a priority to help order the backlog</p>
              </div>

              <div className="bg-gray-50 rounded-lg px-5 py-5">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm font-semibold text-gray-800">
                    Acceptance Criteria <span className="text-red-600">*</span> (minimum 1 required)
                  </span>
                  <button
                    type="button"
                    onClick={handleAddCriterion}
                    className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-purple-600 bg-white border border-purple-600 rounded-md transition-all hover:bg-purple-50"
                  >
                    <span>➕ Add Criterion</span>
                  </button>
                </div>

                <div className="flex flex-col gap-3">
                  {criteria.map((criterion, index) => (
                    <div key={index} className="flex gap-3 items-start">
                      <input
                        type="text"
                        value={criterion}
                        onChange={(e) => handleCriterionChange(index, e.target.value)}
                        placeholder="Describe a specific, testable acceptance criterion"
                        className="flex-1 px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
                      />
                      <button
                        type="button"
                        onClick={() => handleRemoveCriterion(index)}
                        className="w-9 h-9 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 transition-all hover:bg-red-50 hover:border-red-300 hover:text-red-700 flex-shrink-0"
                        title="Remove criterion"
                      >
                        <span>✕</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="px-8 py-6 border-t border-gray-300 flex gap-3 justify-end">
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-3 text-base font-semibold text-gray-600 bg-white border-2 border-gray-300 rounded-lg transition-all hover:bg-gray-50 hover:border-gray-400"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="inline-flex items-center gap-2 px-6 py-3 text-base font-semibold text-white rounded-lg transition-all hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)] active:translate-y-0"
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}
              >
                <span>💾 Save Story</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
