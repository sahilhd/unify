import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Features', path: '/features' },
  { name: 'Pricing', path: '/pricing' },
  { name: 'Quickstart', path: '/quickstart' },
];

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  return (
    <nav className="w-full backdrop-blur-md bg-gray-900/70 border-b border-gray-800 shadow-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer select-none" onClick={() => navigate('/')}> 
          <span className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-purple-600 tracking-tight font-sans">UniLLM</span>
        </div>
        <div className="flex items-center gap-1 md:gap-3">
          {navLinks.map(link => (
            <button
              key={link.name}
              onClick={() => navigate(link.path)}
              className={`px-4 py-2 rounded-full font-medium transition-all duration-200 text-sm md:text-base
                ${location.pathname === link.path ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg border border-purple-400' : 'text-gray-300 hover:bg-gray-800/70 hover:text-white'}`}
              style={location.pathname === link.path ? { borderWidth: 2, borderImage: 'linear-gradient(90deg, #a78bfa, #60a5fa) 1' } : {}}
            >
              {link.name}
            </button>
          ))}
          <button
            className="px-4 py-2 rounded-full font-medium text-sm md:text-base text-gray-300 hover:bg-gray-800/70 hover:text-white transition-all duration-200"
            onClick={() => window.open('https://github.com/sahilhd/unify', '_blank')}
          >
            GitHub
          </button>
          <button
            className="ml-2 px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-white font-semibold shadow-lg transition-all duration-200 border-2 border-transparent hover:border-purple-400"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        </div>
      </div>
    </nav>
  );
} 