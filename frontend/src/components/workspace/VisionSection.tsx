// Using simple div icons instead of lucide-react

interface VisionSectionProps {
  productName: string;
  productDescription: string;
  visionStatement: string;
  targetProblem: string;
  businessGoals: string;
  successMeasures: string;
  onFieldChange: (field: string, value: string) => void;
}

export default function VisionSection({
  productName,
  productDescription,
  visionStatement,
  targetProblem,
  businessGoals,
  successMeasures,
  onFieldChange
}: VisionSectionProps) {
  return (
    <div>
      {/* Product Identity Section */}
      <div className="bg-white rounded-xl px-8 py-8 border border-gray-300 mb-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center text-xl">
            📄
          </div>
          <h2 className="text-xl font-bold text-gray-900">Product Identity</h2>
        </div>

        <div className="mb-6">
          <label htmlFor="productName" className="block text-sm font-semibold text-gray-800 mb-2">
            Product Name
          </label>
          <input
            type="text"
            id="productName"
            name="productName"
            value={productName}
            onChange={(e) => onFieldChange('productName', e.target.value)}
            placeholder="Enter your product name"
            className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)]"
          />
        </div>

        <div>
          <label htmlFor="productDescription" className="block text-sm font-semibold text-gray-800 mb-2">
            Product Description
          </label>
          <textarea
            id="productDescription"
            name="productDescription"
            value={productDescription}
            onChange={(e) => onFieldChange('productDescription', e.target.value)}
            placeholder="Brief description of what your product does"
            className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[120px] leading-relaxed"
          />
        </div>
      </div>

      {/* Vision & Strategy Section */}
      <div className="bg-white rounded-xl px-8 py-8 border border-gray-300 mb-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center text-xl">
            💡
          </div>
          <h2 className="text-xl font-bold text-gray-900">Vision & Strategy</h2>
        </div>

        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <label htmlFor="visionStatement" className="text-sm font-semibold text-gray-800">
              Vision Statement
            </label>
            <span className="text-xs text-gray-500 italic">What is the ultimate goal of this product?</span>
          </div>
          <textarea
            id="visionStatement"
            name="visionStatement"
            value={visionStatement}
            onChange={(e) => onFieldChange('visionStatement', e.target.value)}
            placeholder="Describe the long-term vision for your product"
            className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[120px] leading-relaxed"
          />
          <p className="mt-1.5 text-xs text-gray-500">Think about the impact you want to create and the change you want to drive.</p>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-2">
            <label htmlFor="targetProblem" className="text-sm font-semibold text-gray-800">
              Target Problem
            </label>
            <span className="text-xs text-gray-500 italic">What problem are you solving?</span>
          </div>
          <textarea
            id="targetProblem"
            name="targetProblem"
            value={targetProblem}
            onChange={(e) => onFieldChange('targetProblem', e.target.value)}
            placeholder="Describe the core problem your product addresses"
            className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[120px] leading-relaxed"
          />
          <p className="mt-1.5 text-xs text-gray-500">Be specific about the pain points your users experience today.</p>
        </div>
      </div>

      {/* Business Goals & Success Section */}
      <div className="bg-white rounded-xl px-8 py-8 border border-gray-300 mb-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center text-xl">
            🎯
          </div>
          <h2 className="text-xl font-bold text-gray-900">Business Goals & Success</h2>
        </div>

        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <label htmlFor="businessGoals" className="text-sm font-semibold text-gray-800">
              Business Goals
            </label>
            <span className="text-xs text-gray-500 italic">What business outcomes do you want to achieve?</span>
          </div>
          <textarea
            id="businessGoals"
            name="businessGoals"
            value={businessGoals}
            onChange={(e) => onFieldChange('businessGoals', e.target.value)}
            placeholder="List your key business objectives"
            className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[120px] leading-relaxed"
          />
          <p className="mt-1.5 text-xs text-gray-500">Focus on measurable business outcomes, not just features.</p>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-2">
            <label htmlFor="successMeasures" className="text-sm font-semibold text-gray-800">
              MVP Success Measures
            </label>
            <span className="text-xs text-gray-500 italic">How will you know if your MVP is successful?</span>
          </div>
          <textarea
            id="successMeasures"
            name="successMeasures"
            value={successMeasures}
            onChange={(e) => onFieldChange('successMeasures', e.target.value)}
            placeholder="Define specific, measurable success criteria"
            className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg transition-all focus:outline-none focus:border-purple-600 focus:shadow-[0_0_0_3px_rgba(102,126,234,0.1)] resize-vertical min-h-[120px] leading-relaxed"
          />
          <p className="mt-1.5 text-xs text-gray-500">Include quantitative metrics and qualitative indicators.</p>
        </div>
      </div>
    </div>
  );
}
