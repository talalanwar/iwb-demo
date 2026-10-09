/**
 * Onboarding/Welcome page component.
 * 
 * Introduces new users to Product Learning Studio features and workflow.
 */

import { useNavigate } from 'react-router-dom';

export default function OnboardingPage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/workspace');
  };

  const handleSkip = () => {
    navigate('/workspace');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl p-12 text-center">
        {/* Logo Section */}
        <div className="mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl inline-flex items-center justify-center mb-6">
            <span className="text-white text-3xl font-bold">PLS</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Welcome to Product Learning Studio
          </h1>
          <p className="text-lg text-gray-600">
            Turn your product ideas into structured, reviewable definitions
          </p>
        </div>

        {/* Features Box */}
        <div className="bg-gray-50 rounded-xl p-6 mb-10">
          <div className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">
            What You Can Do
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="flex items-center gap-2 text-sm text-gray-700">
              <span className="text-green-500">✓</span>
              <span>Define product vision</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-700">
              <span className="text-green-500">✓</span>
              <span>Create user stories</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-700">
              <span className="text-green-500">✓</span>
              <span>Prioritize backlog</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-700">
              <span className="text-green-500">✓</span>
              <span>Share for review</span>
            </div>
          </div>
        </div>

        {/* Steps Container */}
        <div className="text-left mb-10">
          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-base flex-shrink-0">
                1
              </div>
              <div className="flex-1">
                <div className="text-base font-bold text-gray-900 mb-1">
                  Create Your Workspace
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Start by creating a workspace for your product. Give it a name and brief description.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-base flex-shrink-0">
                2
              </div>
              <div className="flex-1">
                <div className="text-base font-bold text-gray-900 mb-1">
                  Define Vision & Context
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Capture your product vision, target problem, business goals, and success measures.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-base flex-shrink-0">
                3
              </div>
              <div className="flex-1">
                <div className="text-base font-bold text-gray-900 mb-1">
                  Build Your Backlog
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Add user stories with acceptance criteria and prioritize them for your MVP.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-base flex-shrink-0">
                4
              </div>
              <div className="flex-1">
                <div className="text-base font-bold text-gray-900 mb-1">
                  Review & Share
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Check readiness, fix any gaps, and share your workspace with reviewers for feedback.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={handleGetStarted}
            className="px-8 py-4 text-base font-semibold text-white bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg hover:-translate-y-0.5 hover:shadow-xl transition-all duration-200 inline-flex items-center gap-2"
          >
            <span>🚀</span>
            <span>Get Started</span>
          </button>
          <button
            onClick={handleSkip}
            className="px-8 py-4 text-base font-semibold text-indigo-600 bg-transparent border-2 border-indigo-600 rounded-lg hover:bg-indigo-50 transition-all duration-200"
          >
            Skip
          </button>
        </div>
      </div>
    </div>
  );
}
