import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  CardElement,
  useStripe,
  useElements
} from '@stripe/react-stripe-js';
import { XMarkIcon, CreditCardIcon } from '@heroicons/react/24/outline';
import { API_BASE_URL } from '../utils/config';

interface CreditPackage {
  credits: number;
  price_usd: number;
  discount?: string;
  popular?: boolean;
}

interface CreditPurchaseProps {
  onClose: () => void;
  onSuccess: (creditsAdded: number, amount: number) => void;
}

const PaymentForm: React.FC<{
  selectedPackage: CreditPackage;
  onClose: () => void;
  onSuccess: (creditsAdded: number, amount: number) => void;
}> = ({ selectedPackage, onClose, onSuccess }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saveCard, setSaveCard] = useState(true);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements || !selectedPackage) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const cardElement = elements.getElement(CardElement);
      if (!cardElement) {
        throw new Error('Card element not found');
      }

      // Create payment intent on backend
      const apiKey = localStorage.getItem('unillm_api_key');
      const intentResponse = await fetch(`${API_BASE_URL}/billing/create-payment-intent`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credit_amount: selectedPackage.credits
        }),
      });

      if (!intentResponse.ok) {
        const errorData = await intentResponse.json();
        throw new Error(errorData.detail || 'Failed to create payment intent');
      }

      const { client_secret, payment_intent_id } = await intentResponse.json();

      // Confirm payment with Stripe
      const { error: stripeError, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
        payment_method: {
          card: cardElement,
          billing_details: {
            email: localStorage.getItem('user_email') || undefined,
          },
        },
        setup_future_usage: saveCard ? 'off_session' : undefined, // Save card for future use
      });

      if (stripeError) {
        throw new Error(stripeError.message || 'Payment failed');
      }

      if (paymentIntent?.status === 'succeeded') {
        // Confirm payment on backend
        const confirmResponse = await fetch(`${API_BASE_URL}/billing/confirm-payment`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            payment_intent_id: payment_intent_id
          }),
        });

        if (confirmResponse.ok) {
          const result = await confirmResponse.json();
          onSuccess(selectedPackage.credits, selectedPackage.price_usd);
          onClose();
        } else {
          throw new Error('Failed to confirm payment on server');
        }
      }
    } catch (err: any) {
      setError(err.message || 'Payment failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Order Summary */}
      <div className="bg-gradient-to-r from-purple-900/20 via-blue-900/10 to-fuchsia-900/20 border border-white/10 rounded-xl p-4">
        <h3 className="text-lg font-semibold text-white mb-3">Order Summary</h3>
        <div className="flex justify-between items-center">
          <span className="text-gray-300">{selectedPackage.credits} Credits</span>
          <span className="text-xl font-bold text-white">${selectedPackage.price_usd}</span>
        </div>
      </div>

      {/* Card Information */}
      <div>
        <label className="block text-sm font-medium text-white mb-2">
          Card Information
        </label>
        <div className="bg-white/10 border border-white/20 rounded-lg p-4">
          <CardElement
            options={{
              style: {
                base: {
                  fontSize: '16px',
                  color: '#ffffff',
                  '::placeholder': {
                    color: '#9ca3af',
                  },
                },
              },
            }}
          />
        </div>
      </div>

      {/* Save Card Option */}
      <div className="flex items-center">
        <input
          id="save-card"
          type="checkbox"
          checked={saveCard}
          onChange={(e) => setSaveCard(e.target.checked)}
          className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
        />
        <label htmlFor="save-card" className="ml-2 text-sm text-gray-300">
          Save this card for future purchases
        </label>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          type="button"
          onClick={onClose}
          className="flex-1 px-4 py-2 bg-gray-600/50 hover:bg-gray-600/70 text-white rounded-lg transition-colors"
          disabled={loading}
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={!stripe || loading}
          className="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 text-white rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Processing...
            </>
          ) : (
            <>
              <CreditCardIcon className="h-4 w-4" />
              Pay ${selectedPackage.price_usd}
            </>
          )}
        </button>
      </div>
    </form>
  );
};

const CreditPurchase: React.FC<CreditPurchaseProps> = ({ onClose, onSuccess }) => {
  const [packages, setPackages] = useState<CreditPackage[]>([]);
  const [selectedPackage, setSelectedPackage] = useState<CreditPackage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stripePromise, setStripePromise] = useState<Promise<any> | null>(null);
  const [showPayment, setShowPayment] = useState(false);

  useEffect(() => {
    initializeStripe();
    fetchCreditPackages();
  }, []);

  const initializeStripe = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/billing/stripe-config`);
      if (!response.ok) {
        throw new Error('Failed to get Stripe configuration');
      }
      
      const { publishable_key } = await response.json();
      const stripe = loadStripe(publishable_key);
      setStripePromise(stripe);
    } catch (error) {
      console.error('Failed to initialize Stripe:', error);
      setError('Failed to load payment system');
    }
  };

  const fetchCreditPackages = async () => {
    try {
      // Default packages if endpoint doesn't exist
      const defaultPackages = [
        { credits: 100, price_usd: 10.00 },
        { credits: 500, price_usd: 45.00, discount: '10% off', popular: true },
        { credits: 1000, price_usd: 80.00, discount: '20% off' },
        { credits: 2000, price_usd: 150.00, discount: '25% off' },
        { credits: 5000, price_usd: 350.00, discount: '30% off' },
      ];
      
      setPackages(defaultPackages);
      setSelectedPackage(defaultPackages.find(pkg => pkg.popular) || defaultPackages[0]);
    } catch (error) {
      setError('Failed to load credit packages');
    } finally {
      setLoading(false);
    }
  };

  const handleContinueToPayment = () => {
    if (!selectedPackage) return;
    setShowPayment(true);
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 w-full max-w-md">
          <div className="text-center text-white">Loading...</div>
        </div>
      </div>
    );
  }

  if (!stripePromise) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 w-full max-w-md">
          <div className="text-center">
            <div className="text-red-400 mb-4">Failed to load payment system</div>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 w-full max-w-md backdrop-blur-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-white">
            {showPayment ? 'Complete Purchase' : 'Purchase Credits'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {!showPayment ? (
          <div className="space-y-4">
            {/* Package Selection */}
            <div className="space-y-3">
              {packages.map((pkg) => (
                <div
                  key={pkg.credits}
                  onClick={() => setSelectedPackage(pkg)}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedPackage?.credits === pkg.credits
                      ? 'border-purple-500 bg-purple-500/10'
                      : 'border-white/10 bg-white/5 hover:border-white/20'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="text-white font-medium">{pkg.credits} Credits</div>
                      {pkg.discount && (
                        <div className="text-green-400 text-sm">{pkg.discount}</div>
                      )}
                    </div>
                    <div className="text-right">
                      <div className="text-white font-bold">${pkg.price_usd}</div>
                      {pkg.popular && (
                        <div className="text-purple-400 text-xs">Most Popular</div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            <button
              onClick={handleContinueToPayment}
              disabled={!selectedPackage}
              className="w-full px-4 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 text-white font-medium rounded-lg transition-colors"
            >
              Continue to Payment
            </button>
          </div>
        ) : (
          <Elements stripe={stripePromise}>
            <PaymentForm
              selectedPackage={selectedPackage!}
              onClose={onClose}
              onSuccess={onSuccess}
            />
          </Elements>
        )}
      </div>
    </div>
  );
};

export default CreditPurchase; 