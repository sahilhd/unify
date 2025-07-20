import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';

const EmailVerification: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    if (!token) {
      setStatus('error');
      setMessage('No verification token found in URL');
      return;
    }

    verifyEmail(token);
  }, [searchParams]);

  const verifyEmail = async (token: string) => {
    try {
      const response = await fetch('https://web-production-70deb.up.railway.app/auth/verify-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token })
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('success');
        setMessage('Email verified successfully! You can now close this window.');
      } else {
        setStatus('error');
        setMessage(data.detail || 'Failed to verify email');
      }
    } catch (error) {
      setStatus('error');
      setMessage('Network error. Please try again.');
    }
  };

  const handleClose = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-gray-800 rounded-lg shadow-lg border border-gray-700 p-8">
        <div className="text-center">
          {status === 'verifying' && (
            <>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
              <h2 className="text-xl font-semibold text-white mb-2">Verifying Email</h2>
              <p className="text-gray-400">Please wait while we verify your email address...</p>
            </>
          )}

          {status === 'success' && (
            <>
              <CheckCircleIcon className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-white mb-2">Email Verified!</h2>
              <p className="text-gray-400 mb-6">{message}</p>
              <button
                onClick={handleClose}
                className="bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded-md transition-colors"
              >
                Go to Dashboard
              </button>
            </>
          )}

          {status === 'error' && (
            <>
              <ExclamationCircleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-white mb-2">Verification Failed</h2>
              <p className="text-gray-400 mb-6">{message}</p>
              <button
                onClick={handleClose}
                className="bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded-md transition-colors"
              >
                Go to Dashboard
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmailVerification; 