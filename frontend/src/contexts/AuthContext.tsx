import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { API_BASE_URL } from '../utils/config';

interface User {
  id: string;
  email: string;
  api_key: string;
  credits: number;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const apiKey = localStorage.getItem('unillm_api_key');
    if (apiKey) {
      fetchUserInfo(apiKey);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserInfo = async (apiKey: string) => {
    try {
      console.log('Fetching user info with API key:', apiKey);
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        console.log('User info fetched successfully:', userData);
        setUser(userData);
      } else {
        const errorData = await response.json();
        console.error('Failed to fetch user info:', errorData);
        localStorage.removeItem('unillm_api_key');
      }
    } catch (error) {
      console.error('Error fetching user info:', error);
      localStorage.removeItem('unillm_api_key');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      console.log('Attempting login for:', email);
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Login response:', data);
        localStorage.setItem('unillm_api_key', data.user.api_key);
        setUser(data.user);
        return true;
      } else {
        const errorData = await response.json();
        console.error('Login failed:', errorData);
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const register = async (email: string, password: string): Promise<boolean> => {
    try {
      console.log('Attempting registration for:', email);
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Registration response:', data);
        localStorage.setItem('unillm_api_key', data.api_key);
        setUser(data);
        return true;
      } else {
        const errorData = await response.json();
        console.error('Registration failed:', errorData);
        return false;
      }
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  const logout = () => {
    // Clear chat history for the current user
    const apiKey = localStorage.getItem('unillm_api_key');
    if (apiKey) {
      localStorage.removeItem(`unillm_chat_history_${apiKey}`);
    }
    localStorage.removeItem('unillm_api_key');
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 