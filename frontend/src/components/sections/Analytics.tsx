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
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

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
  const [usageOverTime, setUsageOverTime] = useState<any[]>([]);
  const [chartMetric, setChartMetric] = useState<'requests' | 'tokens' | 'cost'>('requests');

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

  const fetchUsageOverTime = async () => {
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/billing/usage-over-time`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUsageOverTime(data);
      } else {
        setUsageOverTime([]);
      }
    } catch (error) {
      setUsageOverTime([]);
    }
  };

  // Override the context's refreshUsageStats to also update local state
  const handleRefresh = () => {
    fetchUsageStats();
  };

  useEffect(() => {
    fetchUsageStats();
    fetchUsageOverTime();
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
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Usage Chart */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Usage Over Time</h3>
          <div className="mb-4 flex space-x-2">
            <button
              className={`px-3 py-1 rounded-md text-sm font-medium ${chartMetric === 'requests' ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300'}`}
              onClick={() => setChartMetric('requests')}
            >
              Requests
            </button>
            <button
              className={`px-3 py-1 rounded-md text-sm font-medium ${chartMetric === 'tokens' ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300'}`}
              onClick={() => setChartMetric('tokens')}
            >
              Tokens
            </button>
            <button
              className={`px-3 py-1 rounded-md text-sm font-medium ${chartMetric === 'cost' ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300'}`}
              onClick={() => setChartMetric('cost')}
            >
              Cost
            </button>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={usageOverTime} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fill: '#ccc', fontSize: 12 }} />
                <YAxis tick={{ fill: '#ccc', fontSize: 12 }} />
                <Tooltip contentStyle={{ background: '#222', border: 'none', color: '#fff' }} />
                <Legend />
                <Line type="monotone" dataKey={chartMetric} stroke="#a78bfa" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics; 