import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
// Using emoji icons
import { AppShell } from '../components/common/AppShell';
import StoryList from '../components/stories/StoryList';
import StoryEditorDrawer from '../components/stories/StoryEditorDrawer';
import { getWorkspace, updateStories } from '../api/workspaceApi';

export default function BacklogPage() {
  const [stories, setStories] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [editingStory, setEditingStory] = useState<any>(null);

  useEffect(() => {
    loadStories();
  }, []);

  const loadStories = async () => {
    try {
      const data = await getWorkspace();
      setStories((data as any).stories || []);
    } catch (err) {
      setError('Failed to load stories');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddStory = () => {
    setEditingStory(null);
    setIsEditorOpen(true);
  };

  const handleEditStory = (story: any) => {
    setEditingStory(story);
    setIsEditorOpen(true);
  };

  const handleDeleteStory = async (storyId: number) => {
    if (!confirm('Are you sure you want to delete this story?')) {
      return;
    }

    try {
      const updatedStories = stories.filter(s => s.id !== storyId);
      await (updateStories as any)({
        stories: updatedStories.map((s, index) => ({
          id: s.id,
          title: s.title,
          actor: s.actor,
          need_text: s.need_text,
          outcome_text: s.outcome_text,
          priority: s.priority,
          backlog_order: index + 1,
          acceptance_criteria: s.acceptance_criteria.map((c: any) => ({
            criterion_text: c.criterion_text
          }))
        }))
      });
      await loadStories();
    } catch (err) {
      setError('Failed to delete story');
      console.error(err);
    }
  };

  const handleSaveStory = async (story: any) => {
    try {
      let updatedStories: any[];
      
      if (story.id) {
        // Update existing story
        updatedStories = stories.map(s => 
          s.id === story.id ? { ...s, ...story } : s
        );
      } else {
        // Add new story
        const newStory = {
          ...story,
          id: undefined, // Let backend assign ID
          backlog_order: stories.length + 1
        };
        updatedStories = [...stories, newStory];
      }

      await (updateStories as any)({
        stories: updatedStories.map((s, index) => ({
          id: s.id,
          title: s.title,
          actor: s.actor,
          need_text: s.need_text,
          outcome_text: s.outcome_text,
          priority: s.priority,
          backlog_order: index + 1,
          acceptance_criteria: s.acceptance_criteria.map((c: any) => ({
            criterion_text: c.criterion_text
          }))
        }))
      });
      
      await loadStories();
      setIsEditorOpen(false);
    } catch (err) {
      setError('Failed to save story');
      console.error(err);
    }
  };

  if (isLoading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-600">Loading backlog...</div>
        </div>
      </AppShell>
    );
  }

  return (
    <>
      <AppShell>
        <div className="max-w-6xl mx-auto px-8 py-10">
          <div className="flex items-center justify-between mb-8">
            <div className="flex-1">
              <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
                <Link to="/" className="text-purple-600 hover:underline">
                  Dashboard
                </Link>
                <span>&gt;</span>
                <span>Backlog</span>
              </div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">Backlog</h1>
              <p className="text-lg text-gray-600">Create, edit, and prioritize user stories with acceptance criteria</p>
            </div>
            <button
              onClick={handleAddStory}
              className="inline-flex items-center gap-2 px-7 py-3.5 text-lg font-semibold text-white rounded-lg transition-all hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)] active:translate-y-0"
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              }}
            >
              <span>➕ Add New Story</span>
            </button>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-300 rounded-lg px-4 py-3 mb-6">
              <p className="text-red-700 text-sm font-medium">{error}</p>
            </div>
          )}

          {stories.length > 0 ? (
            <StoryList
              stories={stories}
              onEdit={handleEditStory}
              onDelete={handleDeleteStory}
            />
          ) : (
            <div className="bg-white rounded-xl py-16 px-8 text-center border-2 border-dashed border-gray-300">
              <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-purple-100 flex items-center justify-center text-4xl">
                ➕
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">No Stories Yet</h3>
              <p className="text-base text-gray-600 mb-6">
                Get started by creating your first user story
              </p>
              <button
                onClick={handleAddStory}
                className="inline-flex items-center gap-2 px-7 py-3.5 text-lg font-semibold text-white rounded-lg transition-all hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)]"
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}
              >
                <span>➕ Add New Story</span>
              </button>
            </div>
          )}
        </div>
      </AppShell>

      <StoryEditorDrawer
        story={editingStory}
        isOpen={isEditorOpen}
        onClose={() => setIsEditorOpen(false)}
        onSave={handleSaveStory}
      />
    </>
  );
}
