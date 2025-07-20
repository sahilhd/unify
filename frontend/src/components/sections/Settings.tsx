import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  UserIcon,
  EnvelopeIcon,
  ShieldCheckIcon,
  BellIcon,
  GlobeAltIcon,
  CheckCircleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';

const Settings: React.FC = () => {
  const { user } = useAuth();
  const [email, setEmail] = useState(user?.email || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [notifications, setNotifications] = useState(true);
  const [theme, setTheme] = useState('dark');
  
  // Loading states
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isSendingVerification, setIsSendingVerification] = useState(false);
  const [isVerifyingEmail, setIsVerifyingEmail] = useState(false);
  
  // Status messages
  const [passwordMessage, setPasswordMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const [verificationMessage, setVerificationMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const [verificationUrl, setVerificationUrl] = useState<string | null>(null);

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setPasswordMessage({ type: 'error', text: 'New passwords do not match!' });
      return;
    }
    if (newPassword.length < 8) {
      setPasswordMessage({ type: 'error', text: 'Password must be at least 8 characters long!' });
      return;
    }

    setIsChangingPassword(true);
    setPasswordMessage(null);

    try {
      const response = await fetch('https://web-production-70deb.up.railway.app/auth/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user?.api_key}`
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        })
      });

      const data = await response.json();

      if (response.ok) {
        setPasswordMessage({ type: 'success', text: 'Password changed successfully!' });
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
      } else {
        setPasswordMessage({ type: 'error', text: data.detail || 'Failed to change password' });
      }
    } catch (error) {
      setPasswordMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setIsChangingPassword(false);
    }
  };

  const handleSendVerificationEmail = async () => {
    setIsSendingVerification(true);
    setVerificationMessage(null);

    try {
      const response = await fetch('https://web-production-70deb.up.railway.app/auth/send-verification-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user?.api_key}`
        }
      });

      const data = await response.json();

      if (response.ok) {
        setVerificationMessage({ type: 'success', text: 'Verification email sent successfully!' });
        setVerificationUrl(data.verification_url);
      } else {
        setVerificationMessage({ type: 'error', text: data.detail || 'Failed to send verification email' });
      }
    } catch (error) {
      setVerificationMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setIsSendingVerification(false);
    }
  };

  const handleVerifyEmail = async (token: string) => {
    setIsVerifyingEmail(true);
    setVerificationMessage(null);

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
        setVerificationMessage({ type: 'success', text: 'Email verified successfully!' });
        setVerificationUrl(null);
      } else {
        setVerificationMessage({ type: 'error', text: data.detail || 'Failed to verify email' });
      }
    } catch (error) {
      setVerificationMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setIsVerifyingEmail(false);
    }
  };

  // Check if there's a verification token in the URL
  React.useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      handleVerifyEmail(token);
    }
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-gray-400">Manage your account preferences and settings</p>
      </div>

      {/* Email Verification */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Email Verification</h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <EnvelopeIcon className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-white">Email Address</p>
                  <p className="text-sm text-gray-400">{user?.email}</p>
                </div>
              </div>
              <button
                onClick={handleSendVerificationEmail}
                disabled={isSendingVerification}
                className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-2 px-4 rounded-md transition-colors"
              >
                {isSendingVerification ? 'Sending...' : 'Send Verification Email'}
              </button>
            </div>

            {verificationMessage && (
              <div className={`flex items-center p-3 rounded-md ${
                verificationMessage.type === 'success' 
                  ? 'bg-green-900/20 border border-green-500/50' 
                  : 'bg-red-900/20 border border-red-500/50'
              }`}>
                {verificationMessage.type === 'success' ? (
                  <CheckCircleIcon className="h-5 w-5 text-green-400 mr-2" />
                ) : (
                  <ExclamationCircleIcon className="h-5 w-5 text-red-400 mr-2" />
                )}
                <span className={`text-sm ${
                  verificationMessage.type === 'success' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {verificationMessage.text}
                </span>
              </div>
            )}

            {verificationUrl && (
              <div className="bg-blue-900/20 border border-blue-500/50 rounded-md p-3">
                <p className="text-sm text-blue-400 mb-2">
                  Verification URL (for testing - remove in production):
                </p>
                <a 
                  href={verificationUrl}
                  className="text-sm text-blue-300 hover:text-blue-200 break-all"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {verificationUrl}
                </a>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Password Change */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Change Password</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Current Password
              </label>
              <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter current password"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                New Password
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter new password"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Confirm New Password
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Confirm new password"
              />
            </div>

            {passwordMessage && (
              <div className={`flex items-center p-3 rounded-md ${
                passwordMessage.type === 'success' 
                  ? 'bg-green-900/20 border border-green-500/50' 
                  : 'bg-red-900/20 border border-red-500/50'
              }`}>
                {passwordMessage.type === 'success' ? (
                  <CheckCircleIcon className="h-5 w-5 text-green-400 mr-2" />
                ) : (
                  <ExclamationCircleIcon className="h-5 w-5 text-red-400 mr-2" />
                )}
                <span className={`text-sm ${
                  passwordMessage.type === 'success' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {passwordMessage.text}
                </span>
              </div>
            )}

            <div className="pt-4">
              <button
                onClick={handleChangePassword}
                disabled={isChangingPassword}
                className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-2 px-4 rounded-md transition-colors"
              >
                {isChangingPassword ? 'Changing Password...' : 'Change Password'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Account Information */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Account Information</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Account Created
              </label>
              <div className="flex items-center space-x-3">
                <UserIcon className="h-5 w-5 text-gray-400" />
                <span className="text-white">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Current Credits
              </label>
              <div className="flex items-center space-x-3">
                <ShieldCheckIcon className="h-5 w-5 text-gray-400" />
                <span className="text-white">{user?.credits || 0} credits</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  User ID
                </label>
                <p className="text-white font-mono text-sm">{user?.id || 'N/A'}</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  API Key Status
                </label>
                <p className="text-green-400 text-sm">Active</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Rate Limit
                </label>
                <p className="text-white text-sm">{user?.rate_limit_per_minute || 60} requests/minute</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Daily Quota
                </label>
                <p className="text-white text-sm">{user?.daily_quota || 10000} tokens/day</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="bg-gray-800 shadow rounded-lg border border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-white mb-4">Preferences</h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <BellIcon className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-white">Email Notifications</p>
                  <p className="text-sm text-gray-400">Receive notifications about usage and billing</p>
                </div>
              </div>
              <button
                onClick={() => setNotifications(!notifications)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  notifications ? 'bg-purple-600' : 'bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    notifications ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <GlobeAltIcon className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-white">Theme</p>
                  <p className="text-sm text-gray-400">Choose your preferred theme</p>
                </div>
              </div>
              <select
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                className="bg-gray-700 border border-gray-600 rounded-md px-3 py-1 text-white text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="dark">Dark</option>
                <option value="light">Light</option>
                <option value="system">System</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <ShieldCheckIcon className="h-5 w-5 text-red-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-400">Danger Zone</h3>
            <div className="mt-2 text-sm text-red-300">
              <p className="mb-2">
                Once you delete your account, there is no going back. Please be certain.
              </p>
              <button className="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded text-xs transition-colors">
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings; 