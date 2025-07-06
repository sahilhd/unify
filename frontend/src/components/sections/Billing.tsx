import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  PlusIcon,
  CurrencyDollarIcon,
  CreditCardIcon
} from '@heroicons/react/24/outline';
import StripePayment from '../StripePayment';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || 'pk_test_your_key_here');

const Billing: React.FC = () => {
  const { user } = useAuth();
  const [credits, setCredits] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showStripePayment, setShowStripePayment] = useState(false);
  const [selectedPackage, setSelectedPackage] = useState<any>(null);

  useEffect(() => {
    if (user) {
      setCredits(user.credits || 0);
    }
  }, [user]);

  const handlePaymentSuccess = (creditsAdded: number, amount: number) => {
    setCredits(prev => prev + creditsAdded);
    setShowStripePayment(false);
    setSelectedPackage(null);
    alert(`Successfully purchased ${creditsAdded} credits for $${amount}!`);
  };

  const handlePaymentError = (error: string) => {
    alert(`Payment failed: ${error}`);
  };

  const creditPackages = [
    { credits: 100, price_usd: 10, price_per_credit: 0.1, discount_percent: 0, popular: false },
    { credits: 500, price_usd: 45, price_per_credit: 0.09, discount_percent: 10, popular: true },
    { credits: 1000, price_usd: 80, price_per_credit: 0.08, discount_percent: 20, popular: false },
    { credits: 2000, price_usd: 150, price_per_credit: 0.075, discount_percent: 25, popular: false },
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
                key={pkg.credits}
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
                  <div className="text-2xl font-bold text-white">{pkg.credits}</div>
                  <div className="text-sm text-gray-400">credits</div>
                  <div className="mt-2 text-lg font-semibold text-white">${pkg.price_usd}</div>
                  <div className="text-xs text-gray-500">
                    ${pkg.price_per_credit} per credit
                  </div>
                  <button
                    onClick={() => { setSelectedPackage(pkg); setShowStripePayment(true); }}
                    disabled={loading}
                    className="mt-4 w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-2 px-4 rounded-md transition-colors flex items-center justify-center space-x-2"
                  >
                    {loading ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    ) : (
                      <>
                        <CreditCardIcon className="h-4 w-4" />
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

      {/* Stripe Payment Modal */}
      {showStripePayment && selectedPackage && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
            <Elements stripe={stripePromise}>
              <StripePayment
                selectedPackage={selectedPackage}
                onSuccess={handlePaymentSuccess}
                onError={handlePaymentError}
                onCancel={() => { setShowStripePayment(false); setSelectedPackage(null); }}
              />
            </Elements>
          </div>
        </div>
      )}
    </div>
  );
};

export default Billing; 