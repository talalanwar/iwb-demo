import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
// Using emoji icons instead of lucide-react
import { AppShell } from '../components/common/AppShell';
import VisionSection from '../components/workspace/VisionSection';
import { getWorkspace, updateWorkspace } from '../api/workspaceApi';

export default function WorkspacePage() {
  const [workspace, setWorkspace] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<string>('');
  const [error, setError] = useState('');

  // Form fields
  const [productName, setProductName] = useState('');
  const [productDescription, setProductDescription] = useState('');
  const [visionStatement, setVisionStatement] = useState('');
  const [targetProblem, setTargetProblem] = useState('');
  const [businessGoals, setBusinessGoals] = useState('');
  const [successMeasures, setSuccessMeasures] = useState('');

  useEffect(() => {
    loadWorkspace();
  }, []);

  const loadWorkspace = async () => {
    try {
      const data = await getWorkspace();
      setWorkspace(data);
      
      // Backend returns snake_case, populate form fields
      const ws = data.workspace as any;
      setProductName(ws.product_name || '');
      setProductDescription(ws.short_description || '');
      setVisionStatement(ws.vision_statement || '');
      setTargetProblem(ws.target_problem || '');
      setBusinessGoals(ws.business_goals_json ? ws.business_goals_json.join('\n') : '');
      setSuccessMeasures(ws.success_measures_json ? ws.success_measures_json.join('\n') : '');
      
      if (ws.updated_at) {
        setLastSaved(formatRelativeTime(new Date(ws.updated_at)));
      }
    } catch (err) {
      setError('Failed to load workspace');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFieldChange = (field: string, value: string) => {
    switch (field) {
      case 'productName':
        setProductName(value);
        break;
      case 'productDescription':
        setProductDescription(value);
        break;
      case 'visionStatement':
        setVisionStatement(value);
        break;
      case 'targetProblem':
        setTargetProblem(value);
        break;
      case 'businessGoals':
        setBusinessGoals(value);
        break;
      case 'successMeasures':
        setSuccessMeasures(value);
        break;
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setError('');

    try {
      // Backend expects snake_case
      await updateWorkspace({
        product_name: productName,
        short_description: productDescription,
        vision_statement: visionStatement,
        target_problem: targetProblem,
        business_goals_json: businessGoals.split('\n').filter(g => g.trim()),
        success_measures_json: successMeasures.split('\n').filter(m => m.trim())
      } as any);
      
      setLastSaved(formatRelativeTime(new Date()));
      await loadWorkspace(); // Reload to get updated data
    } catch (err) {
      setError('Failed to save workspace');
      console.error(err);
    } finally {
      setIsSaving(false);
    }
  };

  const formatRelativeTime = (date: Date): string => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'just now';
    if (diffMins === 1) return '1 minute ago';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours === 1) return '1 hour ago';
    if (diffHours < 24) return `${diffHours} hours ago`;
    
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays === 1) return '1 day ago';
    return `${diffDays} days ago`;
  };

  if (isLoading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-600">Loading workspace...</div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto px-8 py-10">
        <div className="mb-8">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
            <Link to="/" className="text-purple-600 hover:underline">
              Dashboard
            </Link>
            <span>&gt;</span>
            <span>Vision & Business Context</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Product Vision & Business Context</h1>
          <p className="text-lg text-gray-600 leading-relaxed">
            Define the foundation of your product by capturing the vision, target problem, business goals, and success measures.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-300 rounded-lg px-4 py-3 mb-6">
            <p className="text-red-700 text-sm font-medium">{error}</p>
          </div>
        )}

        <form onSubmit={handleSave}>
          <VisionSection
            productName={productName}
            productDescription={productDescription}
            visionStatement={visionStatement}
            targetProblem={targetProblem}
            businessGoals={businessGoals}
            successMeasures={successMeasures}
            onFieldChange={handleFieldChange}
          />

          <div className="flex items-center gap-4 mt-8 pt-8 border-t border-gray-300">
            <button
              type="submit"
              disabled={isSaving}
              className="inline-flex items-center gap-2 px-7 py-3.5 text-lg font-semibold text-white rounded-lg transition-all hover:transform hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(102,126,234,0.4)] active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              }}
            >
              <span>{isSaving ? 'Saving...' : '💾 Save Changes'}</span>
            </button>
            <Link
              to="/"
              className="inline-flex items-center px-7 py-3.5 text-lg font-semibold text-gray-600 bg-white border-2 border-gray-300 rounded-lg transition-all hover:bg-gray-50 hover:border-gray-400"
            >
              Cancel
            </Link>
          </div>
        </form>

        {lastSaved && (
          <div className="mt-4 flex items-center gap-2 text-sm text-green-700 bg-green-50 rounded-lg px-4 py-2 inline-flex">
            <span>✓ Saved {lastSaved}</span>
          </div>
        )}
      </div>
    </AppShell>
  );
}
