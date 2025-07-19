import React, { useState, useEffect } from 'react';
import { CreditCardIcon, PlusIcon, ArrowPathIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import { API_BASE_URL } from '../../utils/config';

interface BillingData {
  credits: number;
  usage: {
    total_requests: number;
    total_tokens: number;
    total_cost: number;
  };
  invoices: Array<{
    id: string;
    amount: number;
    status: string;
    date: string;
    description: string;
  }>;
}

const Billing: React.FC = () => {
  const [billingData, setBillingData] = useState<BillingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [autoReload, setAutoReload] = useState(false);

  useEffect(() => {
    fetchBillingData();
  }, []);

  const fetchBillingData = async () => {
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${API_BASE_URL}/billing/usage`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setBillingData({
          credits: data.credits || 1000,
          usage: {
            total_requests: data.total_requests || 0,
            total_tokens: data.total_tokens || 0,
            total_cost: data.total_cost || 0,
          },
          invoices: data.invoices || [
            {
              id: 'INV-001',
              amount: 25.00,
              status: 'paid',
              date: '2024-01-15',
              description: 'Credit purchase - 1000 credits',
            },
            {
              id: 'INV-002',
              amount: 15.00,
              status: 'paid',
              date: '2024-01-10',
              description: 'Credit purchase - 500 credits',
            },
          ],
        });
      }
    } catch (error) {
      console.error('Error fetching billing data:', error);
    } finally {
      setLoading(false);
    }
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
          <h1 className="text-3xl font-bold text-white mb-2">Billing & Usage</h1>
          <p className="text-gray-400">Manage your credits, payment methods, and view usage analytics</p>
        </div>
        <button
          onClick={fetchBillingData}
          className="flex items-center gap-2 px-4 py-2 bg-gray-800/50 hover:bg-gray-700/50 text-gray-300 hover:text-white rounded-lg transition-all duration-200 border border-gray-700/50 hover:border-gray-600/50"
        >
          <ArrowPathIcon className="h-4 w-4" />
          Refresh
        </button>
      </div>

      {/* Credit Balance Card */}
      <div className="bg-gradient-to-r from-purple-900/30 via-blue-900/20 to-fuchsia-900/20 border border-white/10 rounded-2xl p-8 shadow-2xl backdrop-blur-lg">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg">
              <CreditCardIcon className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Credit Balance</h2>
              <p className="text-gray-400">Available credits for API usage</p>
            </div>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-200 hover:shadow-glow border-2 border-transparent hover:border-purple-400">
            <PlusIcon className="h-5 w-5" />
            Add Credits
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm">
            <div className="text-3xl font-bold text-white mb-2">{billingData?.credits.toLocaleString()}</div>
            <div className="text-gray-400 text-sm">Available Credits</div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm">
            <div className="text-3xl font-bold text-white mb-2">{billingData?.usage.total_requests.toLocaleString()}</div>
            <div className="text-gray-400 text-sm">Total Requests</div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm">
            <div className="text-3xl font-bold text-white mb-2">${billingData?.usage.total_cost.toFixed(2)}</div>
            <div className="text-gray-400 text-sm">Total Spent</div>
          </div>
        </div>
      </div>

      {/* Payment Method & Auto-Reload */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Payment Method */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-lg">
          <div className="flex items-center gap-3 mb-6">
            <CreditCardIcon className="h-6 w-6 text-purple-400" />
            <h3 className="text-xl font-semibold text-white">Payment Method</h3>
          </div>
          
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 mb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="h-8 w-12 bg-gradient-to-r from-gray-600 to-gray-700 rounded flex items-center justify-center">
                  <span className="text-white text-xs font-mono">••••</span>
                </div>
                <div>
                  <div className="text-white font-medium">•••• •••• •••• 4242</div>
                  <div className="text-gray-400 text-sm">Expires 12/25</div>
                </div>
              </div>
              <button className="text-purple-400 hover:text-purple-300 text-sm font-medium transition-colors">
                Edit
              </button>
            </div>
          </div>
          
          <button className="w-full px-4 py-3 bg-gray-800/50 hover:bg-gray-700/50 text-gray-300 hover:text-white rounded-xl transition-all duration-200 border border-gray-700/50 hover:border-gray-600/50">
            Add New Payment Method
          </button>
        </div>

        {/* Auto-Reload */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-lg">
          <div className="flex items-center gap-3 mb-6">
            <ArrowPathIcon className="h-6 w-6 text-purple-400" />
            <h3 className="text-xl font-semibold text-white">Auto-Reload</h3>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-white font-medium">Auto-reload when credits fall below</div>
                <div className="text-gray-400 text-sm">Automatically purchase credits when your balance is low</div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoReload}
                  onChange={(e) => setAutoReload(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-purple-500 peer-checked:to-blue-500"></div>
              </label>
            </div>
            
            {autoReload && (
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-white font-medium">Threshold</label>
                  <select className="bg-gray-800/50 border border-gray-700/50 text-white rounded-lg px-3 py-1 text-sm">
                    <option>100 credits</option>
                    <option>250 credits</option>
                    <option>500 credits</option>
                    <option>1000 credits</option>
                  </select>
                </div>
                <div className="flex items-center justify-between">
                  <label className="text-white font-medium">Reload Amount</label>
                  <select className="bg-gray-800/50 border border-gray-700/50 text-white rounded-lg px-3 py-1 text-sm">
                    <option>500 credits ($12.50)</option>
                    <option>1000 credits ($25.00)</option>
                    <option>2000 credits ($50.00)</option>
                  </select>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Invoice History */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-lg">
        <div className="flex items-center gap-3 mb-6">
          <DocumentTextIcon className="h-6 w-6 text-purple-400" />
          <h3 className="text-xl font-semibold text-white">Invoice History</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700/50">
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Invoice</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Date</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Description</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Amount</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700/30">
              {billingData?.invoices.map((invoice) => (
                <tr key={invoice.id} className="hover:bg-white/5 transition-colors">
                  <td className="py-4 px-4 text-white font-mono">{invoice.id}</td>
                  <td className="py-4 px-4 text-gray-300">{invoice.date}</td>
                  <td className="py-4 px-4 text-gray-300">{invoice.description}</td>
                  <td className="py-4 px-4 text-white font-semibold">${invoice.amount.toFixed(2)}</td>
                  <td className="py-4 px-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      invoice.status === 'paid' 
                        ? 'bg-green-900/30 text-green-400 border border-green-500/30' 
                        : 'bg-yellow-900/30 text-yellow-400 border border-yellow-500/30'
                    }`}>
                      {invoice.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Billing; 