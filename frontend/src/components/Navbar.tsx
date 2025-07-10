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
    <nav className="w-full bg-gradient-to-r from-gray-900/90 via-gray-800/90 to-gray-900/90 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/')}> 
          <span className="text-2xl font-extrabold text-purple-400 tracking-tight">UniLLM</span>
        </div>
        <div className="flex items-center gap-2 md:gap-4">
          {navLinks.map(link => (
            <button
              key={link.name}
              onClick={() => navigate(link.path)}
              className={`px-3 py-2 rounded-md font-medium transition-colors duration-200 text-sm md:text-base
                ${location.pathname === link.path ? 'bg-purple-600 text-white shadow' : 'text-gray-300 hover:bg-gray-800 hover:text-white'}`}
            >
              {link.name}
            </button>
          ))}
          <button
            className="px-3 py-2 rounded-md font-medium text-sm md:text-base text-gray-300 hover:bg-gray-800 hover:text-white transition-colors duration-200"
            onClick={() => window.open('https://github.com/sahilhd/unify', '_blank')}
          >
            GitHub
          </button>
          <button
            className="ml-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-md text-white font-semibold shadow transition-all duration-200"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        </div>
      </div>
    </nav>
  );
} 