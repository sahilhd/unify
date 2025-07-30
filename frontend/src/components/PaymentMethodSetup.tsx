import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  CardElement,
  useStripe,
  useElements
} from '@stripe/react-stripe-js';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { API_BASE_URL } from '../utils/config';

interface PaymentMethodSetupProps {
  onClose: () => void;
  onSuccess: () => void;
}

const PaymentMethodForm: React.FC<{ onClose: () => void; onSuccess: () => void }> = ({ onClose, onSuccess }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Get the card element
      const cardElement = elements.getElement(CardElement);
      if (!cardElement) {
        throw new Error('Card element not found');
      }

      // Create setup intent on backend
      const apiKey = localStorage.getItem('unillm_api_key');
      const setupResponse = await fetch(`${API_BASE_URL}/billing/create-setup-intent`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (!setupResponse.ok) {
        const errorData = await setupResponse.json();
        throw new Error(errorData.detail || 'Failed to create setup intent');
      }

      const { client_secret } = await setupResponse.json();

      // Confirm the setup intent with the card element
      const { error: stripeError } = await stripe.confirmCardSetup(client_secret, {
        payment_method: {
          card: cardElement,
        }
      });

      if (stripeError) {
        throw new Error(stripeError.message || 'Failed to save payment method');
      }

      // Success!
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to save payment method');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
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

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}

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
          className="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 text-white rounded-lg transition-colors"
        >
          {loading ? 'Saving...' : 'Save Payment Method'}
        </button>
      </div>
    </form>
  );
};

const PaymentMethodSetup: React.FC<PaymentMethodSetupProps> = ({ onClose, onSuccess }) => {
  const [stripePromise, setStripePromise] = useState<Promise<any> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeStripe = async () => {
      try {
        // Get Stripe publishable key from backend
        const response = await fetch(`${API_BASE_URL}/billing/stripe-config`);
        if (!response.ok) {
          throw new Error('Failed to get Stripe configuration');
        }
        
        const { publishable_key } = await response.json();
        const stripe = loadStripe(publishable_key);
        setStripePromise(stripe);
      } catch (error) {
        console.error('Failed to initialize Stripe:', error);
      } finally {
        setLoading(false);
      }
    };

    initializeStripe();
  }, []);

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 w-full max-w-md">
          <div className="text-center text-white">Loading Stripe...</div>
        </div>
      </div>
    );
  }

  if (!stripePromise) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 w-full max-w-md">
          <div className="text-center text-red-400">Failed to load Stripe. Please try again.</div>
          <button
            onClick={onClose}
            className="mt-4 w-full px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 w-full max-w-md backdrop-blur-lg">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-white">Add Payment Method</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        <Elements stripe={stripePromise}>
          <PaymentMethodForm onClose={onClose} onSuccess={onSuccess} />
        </Elements>
      </div>
    </div>
  );
};

export default PaymentMethodSetup; 