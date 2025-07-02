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
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">API Keys</h1>
        <p className="text-gray-400">Manage your API keys and access credentials</p>
      </div>

      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Your API Key</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                API Key
              </label>
              <div className="flex items-center space-x-2">
                <div className="flex-1 bg-gray-700 border border-gray-600 rounded-md px-3 py-2 font-mono text-sm">
                  <span className="text-white">{formatApiKey(user?.api_key || '')}</span>
                </div>
                <button
                  onClick={() => setShowKey(!showKey)}
                  className="p-2 bg-gray-700 hover:bg-gray-600 rounded-md transition-colors"
                >
                  {showKey ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400" />
                  )}
                </button>
                <button
                  onClick={copyToClipboard}
                  className="p-2 bg-gray-700 hover:bg-gray-600 rounded-md transition-colors"
                >
                  {copied ? (
                    <CheckIcon className="h-5 w-5 text-green-400" />
                  ) : (
                    <ClipboardDocumentIcon className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {copied && (
                <p className="mt-1 text-sm text-green-400">API key copied to clipboard!</p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Email
                </label>
                <p className="text-white">{user?.email}</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Created
                </label>
                <p className="text-white">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Usage Instructions</h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-2">Authentication</h4>
              <p className="text-sm text-gray-400 mb-2">
                Include your API key in the Authorization header:
              </p>
              <div className="bg-gray-700 rounded-md p-3 font-mono text-sm">
                <span className="text-purple-400">Authorization:</span> Bearer <span className="text-green-400">your-api-key-here</span>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-2">Example Request</h4>
              <div className="bg-gray-700 rounded-md p-3 font-mono text-sm">
                <div className="text-purple-400">curl -X POST process.env.REACT_APP_API_BASE_URL || '${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}'/chat/completions \</div>
                <div className="text-purple-400 ml-4">-H "Authorization: Bearer <span className="text-green-400">your-api-key</span>" \</div>
                <div className="text-purple-400 ml-4">-H "Content-Type: application/json" \</div>
                <div className="text-purple-400 ml-4">-d &apos;{`{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello!"}]}`}&apos;</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-yellow-900/20 border border-yellow-500/50 rounded-lg p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <KeyIcon className="h-5 w-5 text-yellow-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-400">Security Notice</h3>
            <div className="mt-2 text-sm text-yellow-300">
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