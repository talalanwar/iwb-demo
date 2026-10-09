import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SignInPage from '../pages/SignInPage';

// Mock the useAuth hook
const mockLogin = vi.fn();
const mockNavigate = vi.fn();

vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    login: mockLogin,
    user: null,
    logout: vi.fn(),
  }),
}));

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('SignInPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the sign-in form with default credentials', () => {
    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    expect(screen.getByText('Sign in to Product Learning Studio')).toBeInTheDocument();
    expect(screen.getByLabelText('Email Address')).toHaveValue('demo@example.com');
    expect(screen.getByLabelText('Password')).toHaveValue('demo1234');
  });

  it('renders email and password input fields', () => {
    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByLabelText('Email Address');
    const passwordInput = screen.getByLabelText('Password');

    expect(emailInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(emailInput).toHaveAttribute('type', 'email');
    expect(passwordInput).toHaveAttribute('type', 'password');
  });

  it('allows user to change email and password fields', () => {
    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByLabelText('Email Address') as HTMLInputElement;
    const passwordInput = screen.getByLabelText('Password') as HTMLInputElement;

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'testpass123' } });

    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('testpass123');
  });

  it('calls login function on form submit with correct credentials', async () => {
    mockLogin.mockResolvedValue(undefined);

    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'demo@example.com',
        password: 'demo1234',
      });
    });
  });

  it('navigates to workspace page on successful login', async () => {
    mockLogin.mockResolvedValue(undefined);

    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/workspace');
    });
  });

  it('displays error message on login failure', async () => {
    mockLogin.mockRejectedValue(new Error('Invalid credentials'));

    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid email or password. Please try again.')).toBeInTheDocument();
    });
  });

  it('disables submit button while loading', async () => {
    mockLogin.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /signing in/i })).toBeDisabled();
    });
  });

  it('validates email field is required', () => {
    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByLabelText('Email Address');
    expect(emailInput).toHaveAttribute('required');
  });

  it('validates password field has minimum length', () => {
    render(
      <BrowserRouter>
        <SignInPage />
      </BrowserRouter>
    );

    const passwordInput = screen.getByLabelText('Password');
    expect(passwordInput).toHaveAttribute('minLength', '8');
  });
});
