import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LoginSuccess: React.FC = () => {
  const navigate = useNavigate();
  const { setUser } = useAuth();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const apiKey = params.get('api_key');
    if (token && apiKey) {
      localStorage.setItem('unillm_jwt', token);
      localStorage.setItem('unillm_api_key', apiKey);
      // Optionally, fetch user info and update context
      if (setUser) {
        fetch(`${process.env.REACT_APP_API_BASE_URL || 'https://unify-production-82fc.up.railway.app'}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
        })
          .then(res => res.json())
          .then(user => setUser(user))
          .catch(() => {});
      }
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  }, [navigate, setUser]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md text-white text-center">
        <h2 className="text-2xl font-bold mb-4">Logging you in...</h2>
        <p>Please wait while we complete your login.</p>
      </div>
    </div>
  );
};

export default LoginSuccess; 