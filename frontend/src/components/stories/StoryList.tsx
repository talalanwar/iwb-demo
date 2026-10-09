import StoryCard from './StoryCard';

interface StoryListProps {
  stories: Array<{
    id: number;
    title: string;
    actor: string;
    need_text: string;
    outcome_text: string;
    priority: string | null;
    acceptance_criteria: Array<{ id: number; criterion_text: string }>;
  }>;
  onEdit: (story: any) => void;
  onDelete: (storyId: number) => void;
}

export default function StoryList({ stories, onEdit, onDelete }: StoryListProps) {
  return (
    <div className="flex flex-col gap-4">
      {stories.map((story) => (
        <StoryCard
          key={story.id}
          story={story}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
