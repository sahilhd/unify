import React from 'react';
import { useNavigate } from 'react-router-dom';

const features = [
  {
    title: 'Unified LLM API',
    description: 'Access multiple LLM providers (OpenAI, Anthropic, Gemini, Mistral, Cohere) with a single API and SDK.',
    icon: '🤖',
  },
  {
    title: 'Flexible Billing',
    description: 'Pay-as-you-go credits, Stripe integration, and transparent usage analytics.',
    icon: '💳',
  },
  {
    title: 'Production-Ready',
    description: 'FastAPI backend, React frontend, robust authentication, and scalable deployment.',
    icon: '🚀',
  },
  {
    title: 'Open Source',
    description: 'MIT-licensed, extensible, and developer-friendly.',
    icon: '🌐',
  },
];

export default function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen flex flex-col">
      <nav className="flex justify-between items-center px-8 py-6">
        <div className="text-2xl font-bold text-purple-400 cursor-pointer" onClick={() => navigate('/')}>UniLLM</div>
        <div className="space-x-6">
          <button className="text-white hover:text-purple-400" onClick={() => navigate('/features')}>Features</button>
          <button className="text-white hover:text-purple-400" onClick={() => navigate('/pricing')}>Pricing</button>
          <button className="text-white hover:text-purple-400" onClick={() => navigate('/quickstart')}>Quickstart</button>
          <button className="text-white hover:text-purple-400" onClick={() => window.open('https://github.com/sahilhd/unify', '_blank')}>GitHub</button>
          <button className="ml-4 px-4 py-2 bg-purple-500 hover:bg-purple-600 rounded text-white font-semibold shadow" onClick={() => navigate('/login')}>Login</button>
        </div>
      </nav>
      <main className="flex-1 flex flex-col items-center justify-center text-center px-4">
        <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-6">Unify Your LLM Experience</h1>
        <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-2xl">A unified API gateway and SDK for all your large language model needs. Simple, scalable, and open source.</p>
        <div className="flex flex-col md:flex-row gap-4 mb-12">
          <button className="px-8 py-3 bg-purple-500 hover:bg-purple-600 rounded text-lg font-semibold text-white shadow" onClick={() => navigate('/login')}>Get Started</button>
          <button className="px-8 py-3 bg-gray-700 hover:bg-gray-600 rounded text-lg font-semibold text-white shadow" onClick={() => window.open('https://github.com/sahilhd/unify', '_blank')}>View on GitHub</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {features.map((feature) => (
            <div key={feature.title} className="bg-gray-800 rounded-lg p-6 shadow-lg flex items-center gap-4">
              <span className="text-4xl">{feature.icon}</span>
              <div className="text-left">
                <h3 className="text-xl font-bold text-purple-300 mb-1">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </main>
      <footer className="text-center text-gray-500 py-6 text-sm">© {new Date().getFullYear()} UniLLM. All rights reserved.</footer>
    </div>
  );
} 