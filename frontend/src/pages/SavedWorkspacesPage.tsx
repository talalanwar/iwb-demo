/**
 * Saved Workspaces page component.
 * 
 * Displays a list of all user workspaces with management actions.
 * Note: MVP supports single workspace per user, but UI shows list pattern for learning purposes.
 */

import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function SavedWorkspacesPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/sign-in');
  };

  const handleOpenWorkspace = () => {
    navigate('/workspace');
  };

  const handleCreateWorkspace = () => {
    navigate('/workspace');
  };

  // Sample workspaces for display (in MVP, user has only one workspace)
  const workspaces = [
    {
      id: 1,
      title: 'Product Learning Studio',
      description: 'A browser-based demo SaaS application that helps product learners turn rough ideas into structured, reviewable product definitions.',
      updatedAt: '2 minutes ago',
      storyCount: 8,
      readiness: 75,
      status: 'incomplete'
    },
    {
      id: 2,
      title: 'Mobile Banking App',
      description: 'A secure mobile banking application for retail customers to manage accounts, transfer funds, and pay bills.',
      updatedAt: '3 days ago',
      storyCount: 12,
      readiness: 100,
      status: 'ready'
    },
    {
      id: 3,
      title: 'E-Commerce Platform',
      description: 'An online marketplace connecting local artisans with customers seeking handcrafted, sustainable products.',
      updatedAt: '1 week ago',
      storyCount: 15,
      readiness: 60,
      status: 'incomplete'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-base">
              PLS
            </div>
            <span className="text-lg font-bold text-gray-900">Product Learning Studio</span>
          </div>
          <div className="flex items-center gap-6">
            {user && (
              <>
                <span className="text-sm text-gray-700">{user.displayName}</span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-gray-500 hover:text-gray-700"
                >
                  Sign Out
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-8 py-10">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex-1">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">My Workspaces</h1>
            <p className="text-base text-gray-600">Access your saved product workspaces</p>
          </div>
          <button
            onClick={handleCreateWorkspace}
            className="px-7 py-3.5 text-base font-semibold text-white bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg hover:-translate-y-0.5 hover:shadow-xl transition-all duration-200 inline-flex items-center gap-2"
          >
            <span>➕</span>
            <span>Create New Workspace</span>
          </button>
        </div>

        {/* Workspace Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workspaces.map((workspace) => (
            <div
              key={workspace.id}
              className="bg-white rounded-xl p-6 border border-gray-200 hover:shadow-lg hover:border-gray-300 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer"
              onClick={handleOpenWorkspace}
            >
              {/* Workspace Icon */}
              <div className="mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center text-white">
                  <span className="text-2xl">📁</span>
                </div>
              </div>

              {/* Workspace Info */}
              <h3 className="text-xl font-bold text-gray-900 mb-2">{workspace.title}</h3>
              <p className="text-sm text-gray-600 leading-relaxed mb-4 line-clamp-3">
                {workspace.description}
              </p>

              {/* Meta Info */}
              <div className="flex items-center gap-4 text-xs text-gray-500 mb-4">
                <div className="flex items-center gap-1.5">
                  <span>🕐</span>
                  <span>Updated {workspace.updatedAt}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span>📋</span>
                  <span>{workspace.storyCount} stories</span>
                </div>
              </div>

              {/* Status Badge */}
              <div className="mb-4">
                {workspace.status === 'ready' ? (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-full bg-green-50 text-green-700">
                    <span>✓</span>
                    <span>Ready for Review</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-full bg-orange-50 text-orange-700">
                    <span>⚠</span>
                    <span>{workspace.readiness}% Ready</span>
                  </span>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-4 border-t border-gray-200">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleOpenWorkspace();
                  }}
                  className="flex-1 px-5 py-2.5 text-sm font-semibold text-indigo-600 bg-indigo-50 rounded-md hover:bg-indigo-100 transition-colors inline-flex items-center justify-center gap-1.5"
                >
                  <span>📂</span>
                  <span>Open Workspace</span>
                </button>
                <button
                  onClick={(e) => e.stopPropagation()}
                  className="w-9 h-9 flex items-center justify-center bg-transparent border border-gray-200 rounded-md hover:bg-gray-50 hover:border-gray-300 transition-colors text-gray-600"
                  title="Share workspace"
                >
                  <span>🔗</span>
                </button>
                <button
                  onClick={(e) => e.stopPropagation()}
                  className="w-9 h-9 flex items-center justify-center bg-transparent border border-gray-200 rounded-md hover:bg-gray-50 hover:border-gray-300 transition-colors text-gray-600"
                  title="Delete workspace"
                >
                  <span>🗑️</span>
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State (hidden when workspaces exist) */}
        {workspaces.length === 0 && (
          <div className="bg-white rounded-xl p-16 text-center border-2 border-dashed border-gray-200">
            <div className="w-16 h-16 mx-auto mb-6 bg-indigo-50 rounded-full flex items-center justify-center text-indigo-600">
              <span className="text-4xl">📁</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">No Workspaces Yet</h3>
            <p className="text-base text-gray-600 mb-6">
              Create your first workspace to start defining your product
            </p>
            <button
              onClick={handleCreateWorkspace}
              className="px-7 py-3.5 text-base font-semibold text-white bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg hover:-translate-y-0.5 hover:shadow-xl transition-all duration-200 inline-flex items-center gap-2"
            >
              <span>➕</span>
              <span>Create New Workspace</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
