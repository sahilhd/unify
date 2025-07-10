import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

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
    <div className="relative min-h-screen flex flex-col overflow-x-hidden bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800">
      <Navbar />
      {/* Animated blurred gradient accent */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[80vw] h-[40vh] bg-gradient-to-tr from-purple-500/30 via-blue-400/20 to-fuchsia-400/20 rounded-full blur-3xl opacity-60 pointer-events-none animate-pulse z-0" />
      <main className="flex-1 flex flex-col items-center justify-center text-center px-4 z-10 relative">
        <section className="pt-24 pb-16">
          <h1 className="text-6xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-fuchsia-400 mb-6 drop-shadow-lg tracking-tight leading-tight">Unify Your LLM Experience</h1>
          <p className="text-2xl md:text-3xl text-gray-300 mb-12 max-w-3xl mx-auto font-light">A unified API gateway and SDK for all your large language model needs. Simple, scalable, and open source.</p>
          <div className="flex flex-col md:flex-row gap-4 mb-16 justify-center">
            <button className="px-10 py-4 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-lg font-semibold text-white shadow-xl transition-all duration-200" onClick={() => navigate('/login')}>Get Started</button>
            <button className="px-10 py-4 bg-white/10 hover:bg-white/20 rounded-full text-lg font-semibold text-white shadow-xl border border-white/10 transition-all duration-200" onClick={() => window.open('https://github.com/sahilhd/unify', '_blank')}>View on GitHub</button>
          </div>
        </section>
        <section className="w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 mb-24">
          {features.map((feature) => (
            <div key={feature.title} className="backdrop-blur-lg bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl flex items-center gap-5 transition-transform duration-200 hover:scale-[1.03] hover:shadow-3xl">
              <span className="text-5xl md:text-6xl drop-shadow-lg">{feature.icon}</span>
              <div className="text-left">
                <h3 className="text-2xl font-bold text-purple-200 mb-2 tracking-tight">{feature.title}</h3>
                <p className="text-gray-200 text-lg font-light leading-relaxed">{feature.description}</p>
              </div>
            </div>
          ))}
        </section>
        <section className="w-full max-w-3xl mx-auto mb-20">
          <div className="backdrop-blur-lg bg-gradient-to-r from-purple-900/30 via-blue-900/20 to-fuchsia-900/20 border border-white/10 rounded-2xl p-10 shadow-2xl">
            <h2 className="text-3xl font-bold text-purple-300 mb-4 tracking-tight">Why UniLLM?</h2>
            <ul className="list-disc list-inside text-gray-200 text-lg font-light space-y-2 text-left">
              <li>Unified access to all major LLM providers</li>
              <li>Transparent, flexible billing and real-time analytics</li>
              <li>Open source, extensible, and developer-first</li>
              <li>Beautiful dashboard and instant onboarding</li>
            </ul>
          </div>
        </section>
      </main>
      <footer className="text-center text-gray-500 py-8 text-base font-light border-t border-white/10 bg-gradient-to-t from-gray-900/80 to-transparent z-10 relative">
        © {new Date().getFullYear()} UniLLM. All rights reserved.
      </footer>
    </div>
  );
} 