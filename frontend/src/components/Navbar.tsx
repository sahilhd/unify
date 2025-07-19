import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Features', path: '/features' },
  { name: 'Pricing', path: '/pricing' },
  { name: 'Quickstart', path: '/quickstart' },
];

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <nav className="w-full backdrop-blur-md bg-gray-900/70 border-b border-gray-800 shadow-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer select-none group" onClick={() => navigate('/')}> 
          <div className="h-8 w-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center shadow-lg group-hover:shadow-glow transition-all duration-300">
            <span className="text-white text-sm font-bold">U</span>
          </div>
          <span className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-purple-600 tracking-tight font-sans group-hover:from-purple-300 group-hover:via-blue-300 group-hover:to-purple-500 transition-all duration-300">UniLLM</span>
        </div>
        
        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-1 md:gap-3">
          {navLinks.map(link => (
            <button
              key={link.name}
              onClick={() => navigate(link.path)}
              className={`px-4 py-2 rounded-full font-medium transition-all duration-300 text-sm md:text-base
                ${location.pathname === link.path 
                  ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg border border-purple-400 hover:shadow-glow' 
                  : 'text-gray-300 hover:bg-gray-800/70 hover:text-white hover:shadow-soft'}`}
            >
              {link.name}
            </button>
          ))}
          
          <button
            className="px-4 py-2 rounded-full font-medium text-sm md:text-base text-gray-300 hover:bg-gray-800/70 hover:text-white transition-all duration-300"
            onClick={() => window.open('https://github.com/sahilhd/unify', '_blank')}
          >
            GitHub
          </button>
          
          {user ? (
            <button
              className="ml-2 px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-white font-semibold shadow-lg transition-all duration-300 border-2 border-transparent hover:border-purple-400 hover:shadow-glow"
              onClick={() => navigate('/dashboard')}
            >
              Dashboard
            </button>
          ) : (
            <button
              className="ml-2 px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-white font-semibold shadow-lg transition-all duration-300 border-2 border-transparent hover:border-purple-400 hover:shadow-glow"
              onClick={() => navigate('/login')}
            >
              Login
            </button>
          )}
        </div>

        {/* Mobile menu button */}
        <div className="md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-md text-gray-300 hover:text-white hover:bg-gray-800/70 transition-colors"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-800 bg-gray-900/95 backdrop-blur-xl">
          <div className="px-4 py-2 space-y-1">
            {navLinks.map(link => (
              <button
                key={link.name}
                onClick={() => {
                  navigate(link.path);
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-3 py-2 rounded-md font-medium transition-colors
                  ${location.pathname === link.path 
                    ? 'bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-white' 
                    : 'text-gray-300 hover:bg-gray-800/70 hover:text-white'}`}
              >
                {link.name}
              </button>
            ))}
            <button
              className="block w-full text-left px-3 py-2 rounded-md font-medium text-gray-300 hover:bg-gray-800/70 hover:text-white transition-colors"
              onClick={() => {
                window.open('https://github.com/sahilhd/unify', '_blank');
                setMobileMenuOpen(false);
              }}
            >
              GitHub
            </button>
            {user ? (
              <button
                className="block w-full text-left px-3 py-2 rounded-md font-medium bg-gradient-to-r from-purple-500 to-blue-600 text-white"
                onClick={() => {
                  navigate('/dashboard');
                  setMobileMenuOpen(false);
                }}
              >
                Dashboard
              </button>
            ) : (
              <button
                className="block w-full text-left px-3 py-2 rounded-md font-medium bg-gradient-to-r from-purple-500 to-blue-600 text-white"
                onClick={() => {
                  navigate('/login');
                  setMobileMenuOpen(false);
                }}
              >
                Login
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
} 