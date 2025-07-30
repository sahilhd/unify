import React, { useState, useEffect } from 'react';
import { CreditCardIcon, CheckIcon, StarIcon } from '@heroicons/react/24/outline';
import { API_BASE_URL } from '../utils/config';

interface CreditPackage {
  credits: number;
  price_usd: number;
  price_per_credit: number;
  discount_percent: number;
}

interface CreditPurchaseProps {
  onClose: () => void;
  onSuccess: (creditsAdded: number, amount: number) => void;
}

const CreditPurchase: React.FC<CreditPurchaseProps> = ({ onClose, onSuccess }) => {
  const [packages, setPackages] = useState<CreditPackage[]>([]);
  const [selectedPackage, setSelectedPackage] = useState<CreditPackage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCreditPackages();
  }, []);

  const fetchCreditPackages = async () => {
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${API_BASE_URL}/billing/credit-packages`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setPackages(data);
        // Select the most popular package (500 credits) by default
        const popularPackage = data.find((pkg: CreditPackage) => pkg.credits === 500);
        setSelectedPackage(popularPackage || data[0]);
      } else {
        setError('Failed to load credit packages');
      }
    } catch (error) {
      console.error('Error fetching credit packages:', error);
      setError('Network error. Please try again.');
    }
  };

  const handlePurchase = async () => {
    if (!selectedPackage) return;

    setLoading(true);
    setError(null);

    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      
      // Use the simpler direct credit addition endpoint for testing
      const response = await fetch(`${API_BASE_URL}/billing/add-credits`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          amount: selectedPackage.credits,
          payment_method: 'test_payment'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        onSuccess(selectedPackage.credits, selectedPackage.price_usd);
        onClose();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add credits');
      }
    } catch (error) {
      console.error('Error processing purchase:', error);
      setError('Payment processing error. Please try again.');
    } finally {
      setLoading(false);
    }
  };



  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-900/95 border border-white/10 rounded-2xl p-8 max-w-4xl w-full mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Purchase Credits</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {error && (
          <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-4 mb-6">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Credit Packages */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {packages.map((pkg) => (
            <div
              key={pkg.credits}
              className={`relative border rounded-xl p-6 cursor-pointer transition-all duration-200 ${
                selectedPackage?.credits === pkg.credits
                  ? 'border-purple-500 bg-purple-900/20 shadow-glow'
                  : 'border-gray-700/50 bg-white/5 hover:border-gray-600/50 hover:bg-white/10'
              }`}
              onClick={() => setSelectedPackage(pkg)}
            >
              {pkg.discount_percent > 0 && (
                <div className="absolute -top-2 -right-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-xs px-2 py-1 rounded-full font-semibold">
                  {pkg.discount_percent}% OFF
                </div>
              )}
              
              {pkg.credits === 500 && (
                <div className="absolute -top-2 -left-2 bg-yellow-500 text-black text-xs px-2 py-1 rounded-full font-semibold flex items-center gap-1">
                  <StarIcon className="h-3 w-3" />
                  POPULAR
                </div>
              )}

              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">{pkg.credits.toLocaleString()}</div>
                <div className="text-gray-400 text-sm mb-4">credits</div>
                
                <div className="text-2xl font-bold text-white mb-2">${pkg.price_usd}</div>
                <div className="text-gray-400 text-sm mb-4">
                  ${pkg.price_per_credit.toFixed(3)} per credit
                </div>

                {selectedPackage?.credits === pkg.credits && (
                  <div className="flex items-center justify-center text-purple-400">
                    <CheckIcon className="h-5 w-5 mr-2" />
                    Selected
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Payment Method */}
        <div className="bg-white/5 border border-white/10 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <CreditCardIcon className="h-6 w-6 text-purple-400" />
            <h3 className="text-lg font-semibold text-white">Payment Method</h3>
          </div>
          
          <div className="bg-white/5 border border-white/10 rounded-lg p-4">
            <div className="text-center py-2">
              <div className="text-gray-400 text-sm">Test Environment</div>
              <div className="text-gray-500 text-xs">No real charges will be made</div>
            </div>
          </div>
          
          <p className="text-gray-400 text-sm mt-3">
            💡 This is a test environment. No real charges will be made.
          </p>
        </div>

        {/* Order Summary */}
        {selectedPackage && (
          <div className="bg-gradient-to-r from-purple-900/20 via-blue-900/10 to-fuchsia-900/20 border border-white/10 rounded-xl p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-4">Order Summary</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-300">Credits:</span>
                <span className="text-white font-medium">{selectedPackage.credits.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-300">Price per credit:</span>
                <span className="text-white font-medium">${selectedPackage.price_per_credit.toFixed(3)}</span>
              </div>
              {selectedPackage.discount_percent > 0 && (
                <div className="flex justify-between text-green-400">
                  <span>Discount ({selectedPackage.discount_percent}%):</span>
                  <span>-${((selectedPackage.credits * 0.10) - selectedPackage.price_usd).toFixed(2)}</span>
                </div>
              )}
              <div className="border-t border-gray-700/50 pt-3">
                <div className="flex justify-between">
                  <span className="text-white font-semibold">Total:</span>
                  <span className="text-white font-bold text-xl">${selectedPackage.price_usd}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={onClose}
            className="flex-1 px-6 py-3 bg-gray-800/50 hover:bg-gray-700/50 text-gray-300 hover:text-white rounded-xl transition-all duration-200 border border-gray-700/50"
          >
            Cancel
          </button>
          <button
            onClick={handlePurchase}
            disabled={!selectedPackage || loading}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Processing...
              </>
            ) : (
              <>
                <CreditCardIcon className="h-5 w-5" />
                Purchase Credits
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreditPurchase; 