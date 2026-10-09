/**
 * Settings page component.
 * 
 * Allows users to manage profile information, security settings, and account preferences.
 */

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [displayName, setDisplayName] = useState(user?.displayName || 'Product Learner');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleLogout = async () => {
    await logout();
    navigate('/sign-in');
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    // In MVP, settings save would call backend API
    console.log('Saving settings:', { displayName });
    alert('Settings saved successfully!');
  };

  const handleCancel = () => {
    navigate('/workspace');
  };

  const handleDeleteAccount = () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      alert('Account deletion would be processed here');
    }
  };

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
      <div className="max-w-4xl mx-auto px-8 py-10">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
            <Link to="/workspace" className="text-indigo-600 hover:text-indigo-700">
              Dashboard
            </Link>
            <span>›</span>
            <span>Settings</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Settings</h1>
          <p className="text-base text-gray-600">Manage your profile and account preferences</p>
        </div>

        <form onSubmit={handleSave}>
          {/* Profile Information Section */}
          <div className="bg-white rounded-xl p-8 border border-gray-200 mb-6">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-200">
              <div className="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <span className="text-lg">👤</span>
              </div>
              <h2 className="text-xl font-bold text-gray-900">Profile Information</h2>
            </div>

            <div className="space-y-6">
              <div>
                <label htmlFor="displayName" className="block text-sm font-semibold text-gray-700 mb-2">
                  Display Name
                </label>
                <input
                  type="text"
                  id="displayName"
                  name="displayName"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="Your display name"
                  className="w-full px-4 py-3 text-base border-2 border-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100"
                />
                <p className="mt-1.5 text-xs text-gray-500">
                  This name will be visible to reviewers and coaches
                </p>
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={user?.email || 'learner@example.com'}
                  disabled
                  className="w-full px-4 py-3 text-base border-2 border-gray-200 rounded-lg bg-gray-50 text-gray-500 cursor-not-allowed"
                />
                <p className="mt-1.5 text-xs text-gray-500">
                  Email address cannot be changed
                </p>
              </div>
            </div>
          </div>

          {/* Security Section */}
          <div className="bg-white rounded-xl p-8 border border-gray-200 mb-6">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-200">
              <div className="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <span className="text-lg">🔒</span>
              </div>
              <h2 className="text-xl font-bold text-gray-900">Security</h2>
            </div>

            <div className="space-y-6">
              <div>
                <label htmlFor="currentPassword" className="block text-sm font-semibold text-gray-700 mb-2">
                  Current Password
                </label>
                <input
                  type="password"
                  id="currentPassword"
                  name="currentPassword"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Enter your current password"
                  className="w-full px-4 py-3 text-base border-2 border-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div>
                <label htmlFor="newPassword" className="block text-sm font-semibold text-gray-700 mb-2">
                  New Password
                </label>
                <input
                  type="password"
                  id="newPassword"
                  name="newPassword"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Enter a new password"
                  minLength={8}
                  className="w-full px-4 py-3 text-base border-2 border-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100"
                />
                <p className="mt-1.5 text-xs text-gray-500">
                  Password must be at least 8 characters long
                </p>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-semibold text-gray-700 mb-2">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm your new password"
                  minLength={8}
                  className="w-full px-4 py-3 text-base border-2 border-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100"
                />
              </div>
            </div>
          </div>

          {/* Danger Zone Section */}
          <div className="bg-white rounded-xl p-8 border border-gray-200 mb-6">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-200">
              <div className="w-9 h-9 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <span className="text-lg">⚠️</span>
              </div>
              <h2 className="text-xl font-bold text-gray-900">Danger Zone</h2>
            </div>

            <div className="bg-red-50 border border-red-200 rounded-lg p-5">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-lg bg-red-100 text-red-700 flex items-center justify-center">
                  <span className="text-base">🗑️</span>
                </div>
                <h3 className="text-base font-bold text-red-700">Delete Account</h3>
              </div>
              <p className="text-sm text-red-800 leading-relaxed mb-4">
                Permanently delete your account and all associated workspaces. This action cannot be undone. 
                All your product definitions, stories, and review notes will be permanently removed.
              </p>
              <button
                type="button"
                onClick={handleDeleteAccount}
                className="px-5 py-2.5 text-sm font-semibold text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors inline-flex items-center gap-2"
              >
                <span>🗑️</span>
                <span>Delete My Account</span>
              </button>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex gap-3 pt-8 border-t border-gray-200">
            <button
              type="submit"
              className="px-7 py-3.5 text-base font-semibold text-white bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg hover:-translate-y-0.5 hover:shadow-xl transition-all duration-200 inline-flex items-center gap-2"
            >
              <span>💾</span>
              <span>Save Changes</span>
            </button>
            <button
              type="button"
              onClick={handleCancel}
              className="px-7 py-3.5 text-base font-semibold text-gray-700 bg-white border-2 border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-all duration-200"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
