import React, { useState, useEffect, createContext, useContext } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  ChartBarIcon, 
  CurrencyDollarIcon, 
  ChatBubbleLeftRightIcon,
  ClockIcon,
  ArrowUpIcon,
  ArrowDownIcon
} from '@heroicons/react/24/outline';

interface UsageStats {
  total_requests: number;
  total_tokens: number;
  total_cost: number;
  requests_today: number;
  tokens_today: number;
  cost_today: number;
}

// Create context for usage stats refresh
interface UsageStatsContextType {
  refreshUsageStats: () => void;
}

const UsageStatsContext = createContext<UsageStatsContextType | undefined>(undefined);

export { UsageStatsContext };

export const useUsageStats = () => {
  const context = useContext(UsageStatsContext);
  if (!context) {
    throw new Error('useUsageStats must be used within a UsageStatsProvider');
  }
  return context;
};

const Analytics: React.FC = () => {
  const [usageStats, setUsageStats] = useState<UsageStats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUsageStats = async () => {
    try {
      console.log('Fetching usage stats...');
      const apiKey = localStorage.getItem('unillm_api_key');
      console.log('API Key:', apiKey ? 'Present' : 'Missing');
      
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/billing/usage`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      console.log('Usage stats response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Usage stats data:', data);
        setUsageStats(data);
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Failed to fetch usage stats:', errorData);
      }
    } catch (error) {
      console.error('Error fetching usage stats:', error);
    } finally {
      setLoading(false);
    }
  };

  // Override the context's refreshUsageStats to also update local state
  const handleRefresh = () => {
    fetchUsageStats();
  };

  useEffect(() => {
    fetchUsageStats();
  }, []);

  const stats = [
    {
      name: 'Total Requests',
      value: usageStats?.total_requests || 0,
      icon: ChatBubbleLeftRightIcon,
      change: '+12%',
      changeType: 'positive',
    },
    {
      name: 'Total Tokens',
      value: usageStats?.total_tokens || 0,
      icon: ChartBarIcon,
      change: '+8%',
      changeType: 'positive',
    },
    {
      name: 'Total Cost',
      value: `$${(usageStats?.total_cost || 0).toFixed(4)}`,
      icon: CurrencyDollarIcon,
      change: '+8%',
      changeType: 'positive',
    },
    {
      name: 'Requests Today',
      value: usageStats?.requests_today || 0,
      icon: ClockIcon,
      change: '+5%',
      changeType: 'positive',
    },
    {
      name: 'Cost Today',
      value: `$${(usageStats?.cost_today || 0).toFixed(4)}`,
      icon: ChartBarIcon,
      change: '+3%',
      changeType: 'positive',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Analytics</h1>
            <p className="text-gray-400">Monitor your API usage and costs</p>
          </div>
          <button
            onClick={handleRefresh}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
          >
            <ArrowUpIcon className="h-4 w-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5">
        {stats.map((item) => (
          <div
            key={item.name}
            className="bg-gray-800 overflow-hidden shadow rounded-lg border border-gray-700"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <item.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-400 truncate">
                      {item.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-white">
                        {item.value}
                      </div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        item.changeType === 'positive' ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {item.changeType === 'positive' ? (
                          <ArrowUpIcon className="self-center flex-shrink-0 h-4 w-4" />
                        ) : (
                          <ArrowDownIcon className="self-center flex-shrink-0 h-4 w-4" />
                        )}
                        <span className="sr-only">
                          {item.changeType === 'positive' ? 'Increased' : 'Decreased'} by
                        </span>
                        {item.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Usage Chart Placeholder */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white">Usage Over Time</h3>
          <div className="mt-2 max-w-xl text-sm text-gray-400">
            <p>Detailed usage analytics and charts coming soon...</p>
          </div>
          <div className="mt-5">
            <div className="h-64 bg-gray-700 rounded-md flex items-center justify-center">
              <div className="text-center">
                <ChartBarIcon className="mx-auto h-12 w-12 text-gray-500" />
                <p className="mt-2 text-sm text-gray-400">Chart visualization</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white">Recent Activity</h3>
          <div className="mt-2 max-w-xl text-sm text-gray-400">
            <p>Your recent API requests and usage patterns</p>
          </div>
          <div className="mt-5">
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-700 rounded-md">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-purple-500 rounded-full flex items-center justify-center">
                      <ChatBubbleLeftRightIcon className="h-4 w-4 text-white" />
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-white">Chat completion request</p>
                    <p className="text-sm text-gray-400">gpt-3.5-turbo • 2 minutes ago</p>
                  </div>
                </div>
                <div className="text-sm text-gray-400">$0.002</div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-gray-700 rounded-md">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center">
                      <ChatBubbleLeftRightIcon className="h-4 w-4 text-white" />
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-white">Chat completion request</p>
                    <p className="text-sm text-gray-400">claude-3-sonnet • 5 minutes ago</p>
                  </div>
                </div>
                <div className="text-sm text-gray-400">$0.015</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics; 