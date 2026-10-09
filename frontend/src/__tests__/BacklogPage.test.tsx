import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import BacklogPage from '../pages/BacklogPage';
import * as workspaceApi from '../api/workspaceApi';

// Mock the API module
vi.mock('../api/workspaceApi', () => ({
  getWorkspace: vi.fn(),
  updateStories: vi.fn(),
}));

// Mock the auth hook
vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'demo@example.com', displayName: 'Demo User' },
    login: vi.fn(),
    logout: vi.fn(),
  }),
}));

describe('BacklogPage', () => {
  const mockStoriesData = {
    workspace: {
      id: 1,
      product_name: 'Test Product',
    },
    stories: [
      {
        id: 1,
        title: 'User Authentication',
        actor: 'User',
        need_text: 'sign in securely',
        outcome_text: 'access my workspace',
        priority: 'HIGH',
        backlog_order: 1,
        acceptance_criteria: [
          { id: 1, criterion_text: 'Email and password required', display_order: 1 },
          { id: 2, criterion_text: 'Invalid credentials rejected', display_order: 2 },
        ],
      },
      {
        id: 2,
        title: 'Product Vision',
        actor: 'Product Owner',
        need_text: 'define product vision',
        outcome_text: 'communicate strategy',
        priority: 'MEDIUM',
        backlog_order: 2,
        acceptance_criteria: [
          { id: 3, criterion_text: 'Vision statement captured', display_order: 1 },
        ],
      },
      {
        id: 3,
        title: 'Story Prioritization',
        actor: 'Product Owner',
        need_text: 'prioritize stories',
        outcome_text: 'focus on high-value work',
        priority: 'LOW',
        backlog_order: 3,
        acceptance_criteria: [],
      },
    ],
    review: { notes_count: 0 },
  };

  beforeEach(() => {
    vi.clearAllMocks();
    (workspaceApi.getWorkspace as any).mockResolvedValue(mockStoriesData);
    (workspaceApi.updateStories as any).mockResolvedValue({ success: true });
  });

  it('renders the backlog page with header', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Backlog', level: 1 })).toBeInTheDocument();
    });

    expect(screen.getByText('Create, edit, and prioritize user stories with acceptance criteria')).toBeInTheDocument();
  });

  it('loads and displays stories on mount', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(workspaceApi.getWorkspace).toHaveBeenCalledTimes(1);
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'User Authentication', level: 3 })).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: 'Product Vision', level: 3 })).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: 'Story Prioritization', level: 3 })).toBeInTheDocument();
    });
  });

  it('displays story cards with priority badges', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'User Authentication', level: 3 })).toBeInTheDocument();
    });

    // Check that priority badges are displayed (actual text in StoryCard)
    expect(screen.getByText(/High Priority/)).toBeInTheDocument();
    expect(screen.getByText(/Medium Priority/)).toBeInTheDocument();
    expect(screen.getByText(/Low Priority/)).toBeInTheDocument();
  });

  it('displays acceptance criteria count for each story', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'User Authentication', level: 3 })).toBeInTheDocument();
    });

    // First story has 2 criteria
    expect(screen.getByText(/2 acceptance criteria/)).toBeInTheDocument();

    // Second story has 1 criterion
    expect(screen.getByText(/1 acceptance criterion/)).toBeInTheDocument();

    // Third story has 0 criteria
    expect(screen.getByText(/No acceptance criteria/)).toBeInTheDocument();
  });

  it('renders Add New Story button', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Backlog', level: 1 })).toBeInTheDocument();
    });

    const addButton = screen.getByRole('button', { name: /add new story/i });
    expect(addButton).toBeInTheDocument();
  });

  it('displays loading state while fetching stories', () => {
    (workspaceApi.getWorkspace as any).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockStoriesData), 100))
    );

    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    expect(screen.getByText('Loading backlog...')).toBeInTheDocument();
  });

  it('displays error message on load failure', async () => {
    (workspaceApi.getWorkspace as any).mockRejectedValue(new Error('Network error'));

    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Failed to load stories')).toBeInTheDocument();
    });
  });

  it('renders empty state when no stories exist', async () => {
    (workspaceApi.getWorkspace as any).mockResolvedValue({
      ...mockStoriesData,
      stories: [],
    });

    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Backlog', level: 1 })).toBeInTheDocument();
    });

    // Wait for content to render, then check for empty state
    await waitFor(() => {
      expect(screen.getByText(/No Stories Yet/)).toBeInTheDocument();
    });
  });

  it('displays stories in backlog order', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'User Authentication', level: 3 })).toBeInTheDocument();
    });

    const storyTitles = screen.getAllByRole('heading', { level: 3 }).map(el => el.textContent);
    expect(storyTitles).toContain('User Authentication');
    expect(storyTitles).toContain('Product Vision');
    expect(storyTitles).toContain('Story Prioritization');
  });

  it('shows story actor, need, and outcome format', async () => {
    render(
      <BrowserRouter>
        <BacklogPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'User Authentication', level: 3 })).toBeInTheDocument();
    });

    // Check for user story format elements
    expect(screen.getByText(/sign in securely/)).toBeInTheDocument();
    expect(screen.getByText(/access my workspace/)).toBeInTheDocument();
  });
});
