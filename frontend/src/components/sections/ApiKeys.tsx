import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  KeyIcon,
  ClipboardDocumentIcon,
  CheckIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';

const ApiKeys: React.FC = () => {
  const { user } = useAuth();
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    if (user?.api_key) {
      await navigator.clipboard.writeText(user.api_key);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const formatApiKey = (key: string) => {
    if (!showKey) {
      return '•'.repeat(32);
    }
    return key;
  };

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-fuchsia-400 mb-2 tracking-tight">API Keys</h1>
        <p className="text-lg text-gray-300 font-light">Manage your API keys and access credentials</p>
      </div>

      {/* API Key Card */}
      <div className="relative bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8 shadow-2xl flex flex-col items-center text-center max-w-xl mx-auto">
        <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full px-6 py-2 text-white font-semibold shadow-lg text-lg tracking-wide animate-pulse select-none">
          Your API Key
        </div>
        <div className="mt-8 flex items-center space-x-2 w-full justify-center">
          <div className="flex-1 bg-gray-900/80 border border-white/10 rounded-lg px-4 py-3 font-mono text-lg text-white tracking-wider select-all transition-all duration-200 shadow-inner">
            {formatApiKey(user?.api_key || '')}
          </div>
          <button
            onClick={() => setShowKey(!showKey)}
            className="p-2 bg-gray-900/70 hover:bg-gray-800 rounded-lg transition-colors border border-white/10"
            aria-label={showKey ? 'Hide API key' : 'Show API key'}
          >
            {showKey ? (
              <EyeSlashIcon className="h-6 w-6 text-gray-400" />
            ) : (
              <EyeIcon className="h-6 w-6 text-gray-400" />
            )}
          </button>
          <button
            onClick={copyToClipboard}
            className={`p-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-700 rounded-lg transition-all border border-white/10 shadow-lg ${copied ? 'animate-bounce' : ''}`}
            aria-label="Copy API key"
          >
            {copied ? (
              <CheckIcon className="h-6 w-6 text-green-400" />
            ) : (
              <ClipboardDocumentIcon className="h-6 w-6 text-white" />
            )}
          </button>
        </div>
        {copied && (
          <div className="mt-4 text-green-400 text-base font-semibold animate-fade-in">API key copied to clipboard!</div>
        )}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Email</label>
            <p className="text-white text-lg font-light">{user?.email}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Created</label>
            <p className="text-white text-lg font-light">{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      </div>

      {/* Usage Instructions */}
      <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8 shadow-2xl">
        <h3 className="text-2xl font-bold text-purple-200 mb-4 tracking-tight">Usage Instructions</h3>
        <div className="space-y-6">
          <div>
            <h4 className="text-lg font-semibold text-gray-300 mb-2">Authentication</h4>
            <p className="text-base text-gray-400 mb-2">
              Include your API key in the Authorization header:
            </p>
            <div className="bg-gray-900/80 rounded-lg p-4 font-mono text-base text-white border border-white/10">
              <span className="text-purple-400">Authorization:</span> Bearer <span className="text-green-400">your-api-key-here</span>
            </div>
          </div>
          <div>
            <h4 className="text-lg font-semibold text-gray-300 mb-2">Example Request</h4>
            <div className="bg-gray-900/80 rounded-lg p-4 font-mono text-base text-white border border-white/10">
              <div className="text-purple-400">curl -X POST {process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/chat/completions \</div>
              <div className="text-purple-400 ml-4">-H "Authorization: Bearer <span className="text-green-400">your-api-key</span>" \</div>
              <div className="text-purple-400 ml-4">-H "Content-Type: application/json" \</div>
              <div className="text-purple-400 ml-4">-d '{`{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello!"}]}`}'</div>
            </div>
          </div>
        </div>
      </div>

      {/* Security Notice */}
      <div className="bg-yellow-900/20 border border-yellow-500/50 rounded-2xl p-6 shadow-lg">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <KeyIcon className="h-6 w-6 text-yellow-400" />
          </div>
          <div className="ml-4">
            <h3 className="text-lg font-semibold text-yellow-400">Security Notice</h3>
            <div className="mt-2 text-base text-yellow-300">
              <p>
                Keep your API key secure and never share it publicly. If you suspect your key has been compromised, 
                contact support immediately.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApiKeys; 