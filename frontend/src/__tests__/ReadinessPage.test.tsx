import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ReadinessPage from '../pages/ReadinessPage';
import * as workspaceApi from '../api/workspaceApi';

// Mock the API module
vi.mock('../api/workspaceApi', () => ({
  getReadiness: vi.fn(),
}));

// Mock the auth hook
vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'demo@example.com', displayName: 'Demo User' },
    login: vi.fn(),
    logout: vi.fn(),
  }),
}));

describe('ReadinessPage', () => {
  const mockReadinessDataReady = {
    status: 'READY_FOR_REVIEW',
    summary: {
      readiness_percentage: 100,
      vision_complete: true,
      story_count: 3,
      stories_with_criteria: 3,
      all_stories_have_criteria: true,
      stories_with_priority: 3,
      all_stories_have_priority: true,
      unique_backlog_order: true,
    },
    gaps: [],
  };

  const mockReadinessDataWithGaps = {
    status: 'NEEDS_ATTENTION',
    summary: {
      readiness_percentage: 67,
      vision_complete: true,
      story_count: 3,
      stories_with_criteria: 2,
      all_stories_have_criteria: false,
      stories_with_priority: 3,
      all_stories_have_priority: true,
      unique_backlog_order: true,
    },
    gaps: [
      {
        code: 'MISSING_ACCEPTANCE_CRITERIA',
        message: 'Story "Story Prioritization" is missing acceptance criteria',
        story_id: 3,
        navigate_to: '/backlog?storyId=3&focus=criteria',
      },
    ],
  };

  const mockReadinessDataNotStarted = {
    status: 'NOT_STARTED',
    summary: {
      readiness_percentage: 0,
      vision_complete: false,
      story_count: 0,
      stories_with_criteria: 0,
      all_stories_have_criteria: false,
      stories_with_priority: 0,
      all_stories_have_priority: false,
      unique_backlog_order: true,
    },
    gaps: [
      {
        code: 'MISSING_VISION',
        message: 'Vision statement is required',
        navigate_to: '/workspace#vision',
      },
      {
        code: 'MISSING_STORIES',
        message: 'No stories defined',
        navigate_to: '/backlog',
      },
    ],
  };

  beforeEach(() => {
    vi.clearAllMocks();
    (workspaceApi.getReadiness as any).mockResolvedValue(mockReadinessDataReady);
  });

  it('renders the readiness page with header', async () => {
    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Readiness Summary', level: 1 })).toBeInTheDocument();
    });

    expect(screen.getByText(/Review completeness indicators/)).toBeInTheDocument();
  });

  it('loads and displays readiness data on mount', async () => {
    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(workspaceApi.getReadiness).toHaveBeenCalledTimes(1);
    });

    await waitFor(() => {
      expect(screen.getByText('100%')).toBeInTheDocument();
    });
  });

  it('displays readiness percentage in the score circle', async () => {
    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('100%')).toBeInTheDocument();
    });

    expect(screen.getByText('Ready')).toBeInTheDocument();
  });

  it('shows "Ready for Review" status when readiness is 100%', async () => {
    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Ready for Review')).toBeInTheDocument();
    });

    expect(screen.getByText('Your workspace is ready for review!')).toBeInTheDocument();
  });

  it('displays gaps when readiness is incomplete', async () => {
    (workspaceApi.getReadiness as any).mockResolvedValue(mockReadinessDataWithGaps);

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('67%')).toBeInTheDocument();
    });

    expect(screen.getByText('Almost Ready for Review')).toBeInTheDocument();
    expect(screen.getByText(/Fix 1 gap to complete/)).toBeInTheDocument();
  });

  it('renders gap list with navigation links', async () => {
    (workspaceApi.getReadiness as any).mockResolvedValue(mockReadinessDataWithGaps);

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Story "Story Prioritization" is missing acceptance criteria/)).toBeInTheDocument();
    });

    const fixLinks = screen.getAllByRole('link', { name: /fix in backlog/i });
    expect(fixLinks.length).toBeGreaterThan(0);
  });

  it('displays multiple gaps when many items are incomplete', async () => {
    (workspaceApi.getReadiness as any).mockResolvedValue(mockReadinessDataNotStarted);

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('0%')).toBeInTheDocument();
    });

    expect(screen.getByText(/Fix 2 gaps to complete/)).toBeInTheDocument();
    expect(screen.getByText(/Vision statement is required/)).toBeInTheDocument();
    expect(screen.getByText(/No stories defined/)).toBeInTheDocument();
  });

  it('renders summary cards for vision, stories, and prioritization', async () => {
    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Vision & Context')).toBeInTheDocument();
    });

    expect(screen.getByText('User Stories')).toBeInTheDocument();
    expect(screen.getByText('Prioritization')).toBeInTheDocument();
  });

  it('shows complete status for vision when all fields are filled', async () => {
    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Vision & Context')).toBeInTheDocument();
    });

    // Vision card should show complete status
    const visionCard = screen.getByText('Vision & Context').closest('div');
    expect(visionCard).toBeInTheDocument();
  });

  it('displays loading state while fetching readiness', () => {
    (workspaceApi.getReadiness as any).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockReadinessDataReady), 100))
    );

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    expect(screen.getByText('Loading readiness summary...')).toBeInTheDocument();
  });

  it('displays error message on load failure', async () => {
    (workspaceApi.getReadiness as any).mockRejectedValue(new Error('Network error'));

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Failed to load readiness summary')).toBeInTheDocument();
    });
  });

  it('shows correct status message for IN_PROGRESS state', async () => {
    (workspaceApi.getReadiness as any).mockResolvedValue({
      ...mockReadinessDataWithGaps,
      status: 'IN_PROGRESS',
    });

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('In Progress')).toBeInTheDocument();
    });
  });

  it('renders gap navigation targets correctly', async () => {
    (workspaceApi.getReadiness as any).mockResolvedValue(mockReadinessDataNotStarted);

    render(
      <BrowserRouter>
        <ReadinessPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Vision statement is required/)).toBeInTheDocument();
    });

    const fixLinks = screen.getAllByRole('link');
    const workspaceLink = fixLinks.find(link => link.getAttribute('href')?.includes('/workspace'));
    const backlogLink = fixLinks.find(link => link.getAttribute('href') === '/backlog');

    expect(workspaceLink).toBeDefined();
    expect(backlogLink).toBeDefined();
  });
});
