import React, { useState, useEffect } from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import { useAuth } from '../contexts/AuthContext';

interface CreditPackage {
  credits: number;
  price_usd: number;
  price_per_credit: number;
  discount_percent: number;
}

interface StripePaymentProps {
  selectedPackage: CreditPackage | null;
  onSuccess?: (credits: number, amount: number) => void;
  onError?: (error: string) => void;
  onCancel?: () => void;
}

const StripePayment: React.FC<StripePaymentProps> = ({ selectedPackage, onSuccess, onError, onCancel }) => {
  const { user } = useAuth();
  const stripe = useStripe();
  const elements = useElements();
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (selectedPackage) {
      createPaymentIntent(selectedPackage.credits);
    }
    // eslint-disable-next-line
  }, [selectedPackage]);

  const createPaymentIntent = async (creditAmount: number) => {
    setLoading(true);
    setError(null);
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
        setClientSecret(data.client_secret);
      } else {
        setError('Failed to create payment intent');
      }
    } catch (err) {
      setError('Error creating payment intent');
    } finally {
      setLoading(false);
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    if (!stripe || !elements || !clientSecret || !selectedPackage) {
      setError('Stripe not loaded or missing payment info');
      setLoading(false);
      return;
    }
    const cardElement = elements.getElement(CardElement);
    if (!cardElement) {
      setError('Card element not found');
      setLoading(false);
      return;
    }
    const { error: stripeError, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: cardElement,
        billing_details: {
          email: user?.email,
        },
      },
    });
    if (stripeError) {
      setError(stripeError.message || 'Payment failed');
      setLoading(false);
      onError?.(stripeError.message || 'Payment failed');
      return;
    }
    if (paymentIntent && paymentIntent.status === 'succeeded') {
      try {
        await confirmPayment(paymentIntent.id);
        onSuccess?.(selectedPackage.credits, selectedPackage.price_usd);
      } catch (err) {
        setError('Payment succeeded but failed to confirm with backend');
        onError?.('Payment succeeded but failed to confirm with backend');
      }
    }
    setLoading(false);
  };

  if (!selectedPackage) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-white">Complete Payment</h3>
        <button
          onClick={onCancel}
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
        <form id="payment-form" className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Card Information
            </label>
            <div className="bg-gray-600 border border-gray-500 rounded-md p-3">
              <CardElement options={{ style: { base: { fontSize: '16px', color: '#fff' } } }} />
            </div>
          </div>
          <button
            type="submit"
            disabled={loading || !stripe || !elements || !clientSecret}
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