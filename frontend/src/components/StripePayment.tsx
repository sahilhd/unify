import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { useAuth } from '../contexts/AuthContext';

// Load Stripe (you'll need to set this in your environment)
const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || 'pk_test_your_key_here');

interface CreditPackage {
  credits: number;
  price_usd: number;
  price_per_credit: number;
  discount_percent: number;
}

interface StripePaymentProps {
  onSuccess?: (credits: number, amount: number) => void;
  onError?: (error: string) => void;
}

const StripePayment: React.FC<StripePaymentProps> = ({ onSuccess, onError }) => {
  const { user } = useAuth();
  const [packages, setPackages] = useState<CreditPackage[]>([]);
  const [selectedPackage, setSelectedPackage] = useState<CreditPackage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [clientSecret, setClientSecret] = useState<string | null>(null);

  useEffect(() => {
    fetchCreditPackages();
  }, []);

  const fetchCreditPackages = async () => {
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/billing/credit-packages`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setPackages(data);
      } else {
        setError('Failed to load credit packages');
      }
    } catch (err) {
      setError('Error loading credit packages');
    }
  };

  const createPaymentIntent = async (creditAmount: number) => {
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/billing/create-payment-intent`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ credit_amount: creditAmount }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.client_secret;
      } else {
        throw new Error('Failed to create payment intent');
      }
    } catch (err) {
      throw new Error('Error creating payment intent');
    }
  };

  const confirmPayment = async (paymentIntentId: string) => {
    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/billing/confirm-payment`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ payment_intent_id: paymentIntentId }),
      });

      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error('Failed to confirm payment');
      }
    } catch (err) {
      throw new Error('Error confirming payment');
    }
  };

  const handlePackageSelect = (pkg: CreditPackage) => {
    setSelectedPackage(pkg);
    setError(null);
  };

  const handlePayment = async () => {
    if (!selectedPackage) return;

    setLoading(true);
    setError(null);

    try {
      // Create payment intent
      const clientSecret = await createPaymentIntent(selectedPackage.credits);
      setClientSecret(clientSecret);

      // Load Stripe
      const stripe = await stripePromise;
      if (!stripe) {
        throw new Error('Stripe failed to load');
      }

      // Create card element
      const elements = stripe.elements();
      const cardElement = elements.create('card', {
        style: {
          base: {
            fontSize: '16px',
            color: '#424770',
            '::placeholder': {
              color: '#aab7c4',
            },
          },
          invalid: {
            color: '#9e2146',
          },
        },
      });

      // Mount card element
      const cardContainer = document.getElementById('card-element');
      if (cardContainer) {
        cardElement.mount(cardContainer);
      }

      // Handle form submission
      const handleSubmit = async (event: Event) => {
        event.preventDefault();

        if (!stripe || !elements) {
          return;
        }

        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: cardElement,
            billing_details: {
              email: user?.email,
            },
          },
        });

        if (error) {
          setError(error.message || 'Payment failed');
        } else if (paymentIntent) {
          // Confirm payment with backend
          const result = await confirmPayment(paymentIntent.id);
          
          if (result) {
            onSuccess?.(selectedPackage.credits, selectedPackage.price_usd);
            setSelectedPackage(null);
            setClientSecret(null);
            
            // Clean up
            cardElement.unmount();
          }
        }
      };

      // Add submit handler
      const form = document.getElementById('payment-form');
      if (form) {
        form.addEventListener('submit', handleSubmit);
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Payment failed');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setSelectedPackage(null);
    setClientSecret(null);
    setError(null);
  };

  if (!selectedPackage) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-white">Select Credit Package</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {packages.map((pkg) => (
            <div
              key={pkg.credits}
              className={`relative bg-gray-700 border rounded-lg p-4 cursor-pointer hover:bg-gray-600 transition-colors ${
                pkg.discount_percent > 0 ? 'border-purple-500' : 'border-gray-600'
              }`}
              onClick={() => handlePackageSelect(pkg)}
            >
              {pkg.discount_percent > 0 && (
                <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                  <span className="bg-purple-500 text-white text-xs px-2 py-1 rounded-full">
                    {pkg.discount_percent}% OFF
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
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-white">Complete Payment</h3>
        <button
          onClick={handleCancel}
          className="text-gray-400 hover:text-white"
        >
          Cancel
        </button>
      </div>

      <div className="bg-gray-700 rounded-lg p-4">
        <div className="flex justify-between items-center mb-4">
          <span className="text-gray-300">Selected Package:</span>
          <span className="text-white font-medium">
            {selectedPackage.credits} credits - ${selectedPackage.price_usd}
          </span>
        </div>

        {error && (
          <div className="bg-red-500 text-white p-3 rounded-md mb-4">
            {error}
          </div>
        )}

        <form id="payment-form" className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Card Information
            </label>
            <div
              id="card-element"
              className="bg-gray-600 border border-gray-500 rounded-md p-3"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-2 px-4 rounded-md transition-colors flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Processing...</span>
              </>
            ) : (
              <span>Pay ${selectedPackage.price_usd}</span>
            )}
          </button>
        </form>

        <div className="mt-4 text-xs text-gray-400">
          <p>🔒 Your payment is secured by Stripe</p>
          <p>💳 Test card: 4242 4242 4242 4242</p>
        </div>
      </div>
    </div>
  );
};

export default StripePayment; 