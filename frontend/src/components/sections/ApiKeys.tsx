import React, { useState, useEffect } from 'react';
import { KeyIcon, PlusIcon, EyeIcon, EyeSlashIcon, ClipboardDocumentIcon, TrashIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { API_BASE_URL } from '../../utils/config';

interface ApiKey {
  id: string;
  name: string;
  key: string;
  created_at: string;
  last_used?: string;
  is_active: boolean;
}

const ApiKeys: React.FC = () => {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewKeyModal, setShowNewKeyModal] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [showKeys, setShowKeys] = useState<{ [key: string]: boolean }>({});
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchApiKeys();
  }, []);

  const fetchApiKeys = async () => {
    try {
      setError(null);
      const apiKey = localStorage.getItem('unillm_api_key');
      if (!apiKey) {
        setError('No API key found. Please log in first.');
        setLoading(false);
        return;
      }

      const response = await fetch(`${API_BASE_URL}/api-keys`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setApiKeys(data);
      } else if (response.status === 401) {
        setError('Authentication failed. Please log in again.');
      } else {
        setError('Failed to fetch API keys. Please try again.');
      }
    } catch (error) {
      console.error('Error fetching API keys:', error);
      setError('Network error. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const createApiKey = async () => {
    if (!newKeyName.trim()) return;

    try {
      setError(null);
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${API_BASE_URL}/api-keys`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newKeyName }),
      });

      if (response.ok) {
        const data = await response.json();
        // Update the API key in localStorage
        localStorage.setItem('unillm_api_key', data.key);
        // Refresh the list
        await fetchApiKeys();
        setNewKeyName('');
        setShowNewKeyModal(false);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create API key.');
      }
    } catch (error) {
      console.error('Error creating API key:', error);
      setError('Network error. Please try again.');
    }
  };

  const regenerateApiKey = async (keyId: string) => {
    if (!window.confirm('Are you sure you want to regenerate this API key? The old key will no longer work.')) {
      return;
    }

    try {
      setError(null);
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${API_BASE_URL}/api-keys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Fetch the updated API key
        await fetchApiKeys();
        // Update localStorage with the new key
        const newResponse = await fetch(`${API_BASE_URL}/api-keys`, {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
        });
        if (newResponse.ok) {
          const keys = await newResponse.json();
          if (keys.length > 0) {
            localStorage.setItem('unillm_api_key', keys[0].key);
          }
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to regenerate API key.');
      }
    } catch (error) {
      console.error('Error regenerating API key:', error);
      setError('Network error. Please try again.');
    }
  };

  const copyToClipboard = async (text: string, keyId: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedKey(keyId);
      setTimeout(() => setCopiedKey(null), 2000);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
      setError('Failed to copy to clipboard. Please copy manually.');
    }
  };

  const toggleKeyVisibility = (keyId: string) => {
    setShowKeys(prev => ({
      ...prev,
      [keyId]: !prev[keyId]
    }));
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">API Keys</h1>
          <p className="text-gray-400">Manage your API keys for accessing the UniLLM API</p>
        </div>
        <button
          onClick={() => setShowNewKeyModal(true)}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-200 hover:shadow-glow border-2 border-transparent hover:border-purple-400"
        >
          <PlusIcon className="h-5 w-5" />
          Regenerate Key
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-4 flex items-center gap-3">
          <ExclamationTriangleIcon className="h-5 w-5 text-red-400 flex-shrink-0" />
          <div>
            <p className="text-red-400 font-medium">Error</p>
            <p className="text-red-300 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* API Keys List */}
      <div className="bg-white/5 border border-white/10 rounded-2xl backdrop-blur-lg overflow-hidden">
        {apiKeys.length === 0 ? (
          <div className="p-12 text-center">
            <div className="h-16 w-16 bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <KeyIcon className="h-8 w-8 text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">No API keys found</h3>
            <p className="text-gray-400 mb-6">Please log in to access your API keys</p>
            <button
              onClick={() => window.location.href = '/login'}
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-200 hover:shadow-glow"
            >
              Go to Login
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700/50 bg-white/5">
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">Name</th>
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">API Key</th>
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">Created</th>
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">Last Used</th>
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">Status</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700/30">
                {apiKeys.map((apiKey) => (
                  <tr key={apiKey.id} className="hover:bg-white/5 transition-colors">
                    <td className="py-4 px-6">
                      <div className="text-white font-medium">{apiKey.name}</div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-2">
                        <code className="bg-gray-800/50 border border-gray-700/50 rounded-lg px-3 py-2 text-sm font-mono text-gray-300">
                          {showKeys[apiKey.id] ? apiKey.key : `${apiKey.key.substring(0, 12)}...`}
                        </code>
                        <button
                          onClick={() => toggleKeyVisibility(apiKey.id)}
                          className="p-1 text-gray-400 hover:text-white transition-colors"
                        >
                          {showKeys[apiKey.id] ? (
                            <EyeSlashIcon className="h-4 w-4" />
                          ) : (
                            <EyeIcon className="h-4 w-4" />
                          )}
                        </button>
                        <button
                          onClick={() => copyToClipboard(apiKey.key, apiKey.id)}
                          className="p-1 text-gray-400 hover:text-white transition-colors"
                        >
                          <ClipboardDocumentIcon className="h-4 w-4" />
                        </button>
                        {copiedKey === apiKey.id && (
                          <span className="text-xs text-green-400">Copied!</span>
                        )}
                      </div>
                    </td>
                    <td className="py-4 px-6 text-gray-300 text-sm">
                      {formatDate(apiKey.created_at)}
                    </td>
                    <td className="py-4 px-6 text-gray-300 text-sm">
                      {apiKey.last_used ? formatDate(apiKey.last_used) : 'Never'}
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        apiKey.is_active 
                          ? 'bg-green-900/30 text-green-400 border border-green-500/30' 
                          : 'bg-red-900/30 text-red-400 border border-red-500/30'
                      }`}>
                        {apiKey.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={() => regenerateApiKey(apiKey.id)}
                        className="p-2 text-orange-400 hover:text-orange-300 hover:bg-orange-900/20 rounded-lg transition-all duration-200"
                        title="Regenerate API Key"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Security Notice */}
      <div className="bg-gradient-to-r from-purple-900/20 via-blue-900/10 to-fuchsia-900/20 border border-white/10 rounded-2xl p-6 backdrop-blur-lg">
        <div className="flex items-start gap-4">
          <div className="h-8 w-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center flex-shrink-0">
            <KeyIcon className="h-4 w-4 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">Security Best Practices</h3>
            <ul className="text-gray-300 space-y-1 text-sm">
              <li>• Keep your API keys secure and never share them publicly</li>
              <li>• Regenerate your key immediately if you suspect it has been compromised</li>
              <li>• Use environment variables to store API keys in your applications</li>
              <li>• Monitor your API usage to detect any unauthorized access</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Regenerate Key Modal */}
      {showNewKeyModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-900/95 border border-white/10 rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">Regenerate API Key</h2>
            
            <div className="space-y-4">
              <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-yellow-400 font-medium mb-1">Warning</p>
                    <p className="text-yellow-300 text-sm">
                      Regenerating your API key will invalidate the current key. 
                      Any applications using the old key will stop working immediately.
                    </p>
                  </div>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Key Name
                </label>
                <input
                  type="text"
                  value={newKeyName}
                  onChange={(e) => setNewKeyName(e.target.value)}
                  placeholder="e.g., Production API Key"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700/50 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                />
              </div>
              
              <div className="flex gap-3 pt-4">
                <button
                  onClick={createApiKey}
                  disabled={!newKeyName.trim()}
                  className="flex-1 px-4 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all duration-200"
                >
                  Regenerate Key
                </button>
                <button
                  onClick={() => {
                    setShowNewKeyModal(false);
                    setNewKeyName('');
                  }}
                  className="flex-1 px-4 py-3 bg-gray-800/50 hover:bg-gray-700/50 text-gray-300 hover:text-white rounded-xl transition-all duration-200 border border-gray-700/50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ApiKeys; 