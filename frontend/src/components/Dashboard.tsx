import React, { useState } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { 
  ChartBarIcon, 
  ChatBubbleLeftRightIcon, 
  KeyIcon, 
  CreditCardIcon, 
  Cog6ToothIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../utils/config';
import Analytics, { UsageStatsContext } from './sections/Analytics';
import Chat from './sections/Chat';
import ApiKeys from './sections/ApiKeys';
import Billing from './sections/Billing';
import Settings from './sections/Settings';

const navigation = [
  { name: 'Analytics', href: '/dashboard', icon: ChartBarIcon },
  { name: 'Chat', href: '/dashboard/chat', icon: ChatBubbleLeftRightIcon },
  { name: 'API Keys', href: '/dashboard/api-keys', icon: KeyIcon },
  { name: 'Billing', href: '/dashboard/billing', icon: CreditCardIcon },
  { name: 'Settings', href: '/dashboard/settings', icon: Cog6ToothIcon },
];

const Dashboard: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  // Create UsageStatsProvider component
  const UsageStatsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const fetchUsageStats = async () => {
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
          // Handle usage stats data if needed
        }
      } catch (error) {
        console.error('Error fetching usage stats:', error);
      }
    };

    const refreshUsageStats = () => {
      fetchUsageStats();
    };

    React.useEffect(() => {
      fetchUsageStats();
    }, []);

    const contextValue = {
      refreshUsageStats,
    };

    return (
      <UsageStatsContext.Provider value={contextValue}>
        {children}
      </UsageStatsContext.Provider>
    );
  };

  return (
    <div className="h-screen flex overflow-hidden bg-gray-900">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 flex z-40 md:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-gray-800">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <XMarkIcon className="h-6 w-6 text-white" />
            </button>
          </div>
          <SidebarContent user={user} onLogout={handleLogout} />
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col h-0 flex-1 bg-gray-800">
            <SidebarContent user={user} onLogout={handleLogout} />
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <div className="md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
          <button
            type="button"
            className="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            onClick={() => setSidebarOpen(true)}
          >
            <Bars3Icon className="h-6 w-6" />
          </button>
        </div>

        <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <UsageStatsProvider>
                <Routes>
                  <Route path="/" element={<Analytics />} />
                  <Route path="/chat" element={<Chat />} />
                  <Route path="/api-keys" element={<ApiKeys />} />
                  <Route path="/billing" element={<Billing />} />
                  <Route path="/settings" element={<Settings />} />
                </Routes>
              </UsageStatsProvider>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

interface SidebarContentProps {
  user: any;
  onLogout: () => void;
}

const SidebarContent: React.FC<SidebarContentProps> = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <>
      <div className="flex items-center flex-shrink-0 px-4 py-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-8 w-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-sm font-bold">U</span>
            </div>
          </div>
          <div className="ml-3">
            <h1 className="text-xl font-semibold text-white">UniLLM</h1>
          </div>
        </div>
      </div>

      <div className="mt-5 flex-grow flex flex-col">
        <nav className="flex-1 px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <button
                key={item.name}
                onClick={() => navigate(item.href)}
                className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md w-full transition-colors duration-200 ${
                  isActive
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`}
              >
                <item.icon
                  className={`mr-3 flex-shrink-0 h-6 w-6 ${
                    isActive ? 'text-white' : 'text-gray-400 group-hover:text-gray-300'
                  }`}
                />
                {item.name}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="flex-shrink-0 flex border-t border-gray-700 p-4">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-8 w-8 bg-gray-600 rounded-full flex items-center justify-center">
              <UserIcon className="h-5 w-5 text-gray-300" />
            </div>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-white">{user?.email}</p>
            <p className="text-xs text-gray-400">{user?.credits} credits</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="ml-auto flex-shrink-0 bg-gray-700 p-1 rounded-full text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
        >
          <ArrowRightOnRectangleIcon className="h-5 w-5" />
        </button>
      </div>
    </>
  );
};

export default Dashboard; 