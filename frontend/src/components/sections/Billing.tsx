import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  CreditCardIcon,
  PlusIcon,
  CurrencyDollarIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

const Billing: React.FC = () => {
  const { user } = useAuth();
  const [credits, setCredits] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setCredits(user.credits || 0);
    }
  }, [user]);

  const purchaseCredits = async (amount: number) => {
    setLoading(true);
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/billing/purchase-credits`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ credits: amount }),
      });

      if (response.ok) {
        const data = await response.json();
        setCredits(data.credits);
        alert(`Successfully purchased ${amount} credits!`);
      } else {
        alert('Failed to purchase credits. Please try again.');
      }
    } catch (error) {
      console.error('Error purchasing credits:', error);
      alert('An error occurred while purchasing credits.');
    } finally {
      setLoading(false);
    }
  };

  const creditPackages = [
    { amount: 100, price: 10, popular: false },
    { amount: 500, price: 45, popular: true },
    { amount: 1000, price: 80, popular: false },
    { amount: 2000, price: 150, popular: false },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Billing</h1>
        <p className="text-gray-400">Manage your credits and billing information</p>
      </div>

      {/* Current Balance */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg leading-6 font-medium text-white">Current Balance</h3>
              <p className="mt-1 text-sm text-gray-400">Available credits for API usage</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-white">{credits}</div>
              <div className="text-sm text-gray-400">credits</div>
            </div>
          </div>
        </div>
      </div>

      {/* Purchase Credits */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Purchase Credits</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {creditPackages.map((pkg) => (
              <div
                key={pkg.amount}
                className={`relative bg-gray-700 border rounded-lg p-4 hover:bg-gray-600 transition-colors ${
                  pkg.popular ? 'border-purple-500' : 'border-gray-600'
                }`}
              >
                {pkg.popular && (
                  <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                    <span className="bg-purple-500 text-white text-xs px-2 py-1 rounded-full">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">{pkg.amount}</div>
                  <div className="text-sm text-gray-400">credits</div>
                  <div className="mt-2 text-lg font-semibold text-white">${pkg.price}</div>
                  <div className="text-xs text-gray-500">
                    ${(pkg.price / pkg.amount).toFixed(2)} per credit
                  </div>
                  
                  <button
                    onClick={() => purchaseCredits(pkg.amount)}
                    disabled={loading}
                    className="mt-4 w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-2 px-4 rounded-md transition-colors flex items-center justify-center space-x-2"
                  >
                    {loading ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    ) : (
                      <>
                        <PlusIcon className="h-4 w-4" />
                        <span>Purchase</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Billing History */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Billing History</h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-md">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 bg-green-500 rounded-full flex items-center justify-center">
                    <CurrencyDollarIcon className="h-4 w-4 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-white">Credit Purchase</p>
                  <p className="text-sm text-gray-400">500 credits • 2 days ago</p>
                </div>
              </div>
              <div className="text-sm text-green-400">+$45.00</div>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-gray-700 rounded-md">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <CurrencyDollarIcon className="h-4 w-4 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-white">Credit Purchase</p>
                  <p className="text-sm text-gray-400">100 credits • 1 week ago</p>
                </div>
              </div>
              <div className="text-sm text-green-400">+$10.00</div>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing Information */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Pricing Information</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-2">Model Pricing</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">GPT-3.5 Turbo:</span>
                  <span className="text-white">$0.002/1K tokens</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">GPT-4:</span>
                  <span className="text-white">$0.03/1K tokens</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Claude 3 Sonnet:</span>
                  <span className="text-white">$0.015/1K tokens</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Claude 3 Opus:</span>
                  <span className="text-white">$0.075/1K tokens</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-2">Billing Details</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Billing Cycle:</span>
                  <span className="text-white">Pay-as-you-go</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Payment Method:</span>
                  <span className="text-white">Credit Card</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Invoices:</span>
                  <span className="text-white">Available on request</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Billing; 