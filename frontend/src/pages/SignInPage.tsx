import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export default function SignInPage() {
  const [email, setEmail] = useState('demo@example.com');
  const [password, setPassword] = useState('demo1234');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login({ email, password });
      navigate('/workspace');
    } catch (err) {
      setError('Invalid email or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6" style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-[440px]" style={{
        padding: '48px 40px'
      }}>
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4" style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
          }}>
            <span className="text-white text-3xl font-bold">PLS</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
          <p className="text-gray-600 text-base">Sign in to Product Learning Studio</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-300 rounded-lg px-4 py-3 mb-6">
            <p className="text-red-700 text-sm font-medium">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label htmlFor="email" className="block text-sm font-semibold text-gray-800 mb-2">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="learner@example.com"
              required
              autoComplete="email"
              className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-semibold text-gray-800 mb-2">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              autoComplete="current-password"
              minLength={8}
              className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 text-lg font-semibold text-white rounded-lg transition-all hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)] active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed"
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="text-center mt-5">
          <a
            href="#"
            onClick={(e) => e.preventDefault()}
            className="text-purple-600 text-sm font-medium hover:underline"
          >
            Forgot your password?
          </a>
        </div>

        <div className="text-center mt-8 text-xs text-gray-500">
          Product Learning Studio &copy; 2026
        </div>
      </div>
    </div>
  );
}
