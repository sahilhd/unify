import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';

interface PasswordStrength {
  is_valid: boolean;
  score: number;
  strength: string;
  strength_color: string;
  requirements: {
    [key: string]: {
      met: boolean;
      description: string;
      required?: number;
      current?: number;
    };
  };
  suggestions: string[];
}

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength | null>(null);
  const [checkingPassword, setCheckingPassword] = useState(false);
  const [passwordCache, setPasswordCache] = useState<{[key: string]: PasswordStrength}>({});
  const { login, register } = useAuth();

  // Check password strength as user types (only for registration)
  useEffect(() => {
    if (!isLogin && password.length > 0) {
      // Check cache first
      if (passwordCache[password]) {
        setPasswordStrength(passwordCache[password]);
        return;
      }

      const timeoutId = setTimeout(async () => {
        await checkPasswordStrength(password);
      }, 800); // Increased debounce to 800ms

      return () => clearTimeout(timeoutId);
    } else {
      setPasswordStrength(null);
    }
  }, [password, isLogin, passwordCache]);

  const checkPasswordStrength = async (pwd: string) => {
    if (pwd.length === 0) {
      setPasswordStrength(null);
      return;
    }

    setCheckingPassword(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'https://web-production-70deb.up.railway.app'}/auth/check-password-strength`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: pwd }),
      });

      if (response.ok) {
        const data = await response.json();
        setPasswordStrength(data);
        // Cache the result
        setPasswordCache(prev => ({ ...prev, [pwd]: data }));
      }
    } catch (error) {
      console.error('Error checking password strength:', error);
    } finally {
      setCheckingPassword(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      if (isLogin) {
        const success = await login(email, password);
        if (!success) {
          setError('Invalid credentials');
        } else {
          navigate('/dashboard');
        }
      } else {
        // Registration - check password strength first
        if (passwordStrength && !passwordStrength.is_valid) {
          setError('Password does not meet requirements. Please check the password requirements below.');
          setLoading(false);
          return;
        }

        const success = await register(email, password);
        if (success) {
          setSuccess('Account created successfully! You can now log in.');
          // Clear form after successful registration
          setEmail('');
          setPassword('');
          setPasswordStrength(null);
          // Switch to login mode
          setIsLogin(true);
        } else {
          setError('Registration failed. Please try again.');
        }
      }
    } catch (err: any) {
      // Handle specific error messages from the backend
      if (err.message && err.message.includes('verify your email')) {
        setError('Please verify your email address before logging in. Check your inbox for a verification link.');
      } else if (err.message && err.message.includes('Password must')) {
        setError(err.message);
      } else if (err.message && err.message.includes('Email already registered')) {
        setError('An account with this email already exists. Please use a different email or try logging in.');
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = `${process.env.REACT_APP_API_BASE_URL || 'https://unify-production-82fc.up.railway.app'}/auth/google/login`;
  };

  const getStrengthColor = (color: string) => {
    switch (color) {
      case 'green': return 'text-green-400';
      case 'yellow': return 'text-yellow-400';
      case 'orange': return 'text-orange-400';
      case 'red': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStrengthBarColor = (color: string) => {
    switch (color) {
      case 'green': return 'bg-green-500';
      case 'yellow': return 'bg-yellow-500';
      case 'orange': return 'bg-orange-500';
      case 'red': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Navbar />
      <div className="flex-1 flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 p-8">
          <div className="text-center">
            <div className="mx-auto h-12 w-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">U</span>
            </div>
            <h2 className="mt-6 text-3xl font-bold text-white">
              {isLogin ? 'Welcome back' : 'Create your account'}
            </h2>
            <p className="mt-2 text-sm text-gray-400">
              {isLogin ? 'Sign in to your UniLLM account' : 'Join UniLLM to get started'}
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                  Email address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Enter your email"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-300">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Enter your password"
                />
                
                {/* Password Strength Indicator (only for registration) */}
                {!isLogin && password.length > 0 && (
                  <div className="mt-2 space-y-2">
                    {checkingPassword ? (
                      <div className="text-sm text-gray-400">Checking password strength...</div>
                    ) : passwordStrength && (
                      <>
                        {/* Strength Bar */}
                        <div className="space-y-1">
                          <div className="flex justify-between items-center">
                            <span className="text-sm text-gray-400">Password Strength</span>
                            <span className={`text-sm font-medium ${getStrengthColor(passwordStrength.strength_color)}`}>
                              {passwordStrength.strength} ({passwordStrength.score}/100)
                            </span>
                          </div>
                          <div className="w-full bg-gray-700 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full transition-all duration-300 ${getStrengthBarColor(passwordStrength.strength_color)}`}
                              style={{ width: `${passwordStrength.score}%` }}
                            ></div>
                          </div>
                        </div>

                        {/* Requirements Checklist */}
                        {Object.entries(passwordStrength.requirements).length > 0 && (
                          <div className="space-y-1">
                            <div className="text-sm text-gray-400">Requirements:</div>
                            {Object.entries(passwordStrength.requirements).map(([key, req]) => (
                              <div key={key} className="flex items-center space-x-2">
                                {req.met ? (
                                  <CheckCircleIcon className="h-4 w-4 text-green-400" />
                                ) : (
                                  <ExclamationCircleIcon className="h-4 w-4 text-red-400" />
                                )}
                                <span className={`text-xs ${req.met ? 'text-green-400' : 'text-red-400'}`}>
                                  {req.description}
                                </span>
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Suggestions */}
                        {passwordStrength.suggestions.length > 0 && (
                          <div className="space-y-1">
                            <div className="text-sm text-gray-400">Suggestions:</div>
                            {passwordStrength.suggestions.map((suggestion, index) => (
                              <div key={index} className="text-xs text-yellow-400">
                                • {suggestion}
                              </div>
                            ))}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>

            {error && (
              <div className="flex items-center bg-red-900/20 border border-red-500/50 rounded-md p-3">
                <ExclamationCircleIcon className="h-5 w-5 text-red-400 mr-2" />
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            {success && (
              <div className="flex items-center bg-green-900/20 border border-green-500/50 rounded-md p-3">
                <CheckCircleIcon className="h-5 w-5 text-green-400 mr-2" />
                <p className="text-green-400 text-sm">{success}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                isLogin ? 'Sign in' : 'Create account'
              )}
            </button>

            <div className="text-center">
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin);
                  setError('');
                  setSuccess('');
                }}
                className="text-sm text-gray-400 hover:text-white transition-colors duration-200"
              >
                {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
              </button>
            </div>
          </form>

          <div className="mt-6 flex flex-col items-center">
            <button
              onClick={handleGoogleLogin}
              className="w-full flex items-center justify-center bg-white text-gray-800 font-semibold py-2 px-4 rounded shadow hover:bg-gray-100 transition-colors mb-2"
            >
              <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" className="h-5 w-5 mr-2" />
              Sign in with Google
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage; 