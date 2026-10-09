import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import WorkspacePage from '../pages/WorkspacePage';
import * as workspaceApi from '../api/workspaceApi';

// Mock the API module
vi.mock('../api/workspaceApi', () => ({
  getWorkspace: vi.fn(),
  updateWorkspace: vi.fn(),
}));

// Mock the auth hook
vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'demo@example.com', displayName: 'Demo User' },
    login: vi.fn(),
    logout: vi.fn(),
  }),
}));

describe('WorkspacePage', () => {
  const mockWorkspaceData = {
    workspace: {
      id: 1,
      product_name: 'Test Product',
      short_description: 'A test product description',
      vision_statement: 'To revolutionize testing',
      target_problem: 'Testing is hard',
      business_goals_json: ['Goal 1', 'Goal 2', 'Goal 3'],
      success_measures_json: ['Measure 1', 'Measure 2'],
      updated_at: new Date().toISOString(),
    },
    stories: [],
    review: { notes_count: 0 },
  };

  beforeEach(() => {
    vi.clearAllMocks();
    (workspaceApi.getWorkspace as any).mockResolvedValue(mockWorkspaceData);
    (workspaceApi.updateWorkspace as any).mockResolvedValue({ success: true });
  });

  it('renders the workspace page with form sections', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Product Vision & Business Context', level: 1 })).toBeInTheDocument();
    });
  });

  it('loads and displays workspace data on mount', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(workspaceApi.getWorkspace).toHaveBeenCalledTimes(1);
    });

    await waitFor(() => {
      const productNameInput = screen.getByDisplayValue('Test Product');
      expect(productNameInput).toBeInTheDocument();
    });
  });

  it('populates form fields with workspace data', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument();
      expect(screen.getByDisplayValue('A test product description')).toBeInTheDocument();
      expect(screen.getByDisplayValue('To revolutionize testing')).toBeInTheDocument();
      expect(screen.getByDisplayValue('Testing is hard')).toBeInTheDocument();
    });
  });

  it('displays business goals as newline-separated text', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Check that Goal 1 is present
      expect(screen.getByDisplayValue(/Goal 1/)).toBeInTheDocument();
    });

    // Also check the other goals are present in the document
    expect(screen.getByText(/Goal 2/)).toBeInTheDocument();
    expect(screen.getByText(/Goal 3/)).toBeInTheDocument();
  });

  it('allows user to edit form fields', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument();
    });

    const productNameInput = screen.getByDisplayValue('Test Product') as HTMLInputElement;
    fireEvent.change(productNameInput, { target: { value: 'Updated Product' } });

    expect(productNameInput.value).toBe('Updated Product');
  });

  it('calls updateWorkspace API when form is submitted', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument();
    });

    const saveButton = screen.getByRole('button', { name: /save changes/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(workspaceApi.updateWorkspace).toHaveBeenCalledTimes(1);
    });
  });

  it('sends correct data structure to API on save', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument();
    });

    const productNameInput = screen.getByDisplayValue('Test Product') as HTMLInputElement;
    fireEvent.change(productNameInput, { target: { value: 'New Product Name' } });

    const saveButton = screen.getByRole('button', { name: /save changes/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(workspaceApi.updateWorkspace).toHaveBeenCalledWith(
        expect.objectContaining({
          product_name: 'New Product Name',
          short_description: 'A test product description',
          vision_statement: 'To revolutionize testing',
          target_problem: 'Testing is hard',
          business_goals_json: ['Goal 1', 'Goal 2', 'Goal 3'],
          success_measures_json: ['Measure 1', 'Measure 2'],
        })
      );
    });
  });

  it('displays loading state while fetching workspace', () => {
    (workspaceApi.getWorkspace as any).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockWorkspaceData), 100))
    );

    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    expect(screen.getByText('Loading workspace...')).toBeInTheDocument();
  });

  it('displays error message on load failure', async () => {
    (workspaceApi.getWorkspace as any).mockRejectedValue(new Error('Network error'));

    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Failed to load workspace')).toBeInTheDocument();
    });
  });

  it('displays error message on save failure', async () => {
    (workspaceApi.updateWorkspace as any).mockRejectedValue(new Error('Save failed'));

    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument();
    });

    const saveButton = screen.getByRole('button', { name: /save changes/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText('Failed to save workspace')).toBeInTheDocument();
    });
  });

  it('reloads workspace data after successful save', async () => {
    render(
      <BrowserRouter>
        <WorkspacePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument();
    });

    const saveButton = screen.getByRole('button', { name: /save changes/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      // getWorkspace should be called twice: once on mount, once after save
      expect(workspaceApi.getWorkspace).toHaveBeenCalledTimes(2);
    });
  });
});
