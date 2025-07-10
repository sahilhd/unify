import React from 'react';
import Navbar from './Navbar';

const features = [
  {
    icon: '🤖',
    title: 'Unified LLM API',
    description: 'One API for OpenAI, Anthropic, Gemini, Mistral, Cohere, and more.'
  },
  {
    icon: '🔒',
    title: 'Secure Authentication',
    description: 'Google OAuth, JWT, and API key support for robust security.'
  },
  {
    icon: '📊',
    title: 'Usage Analytics',
    description: 'Track requests, tokens, and costs with beautiful charts.'
  },
  {
    icon: '💳',
    title: 'Flexible Billing',
    description: 'Stripe integration, pay-as-you-go credits, and transparent history.'
  },
  {
    icon: '⚡',
    title: 'Fast & Scalable',
    description: 'Production-ready FastAPI backend and React frontend.'
  },
  {
    icon: '🌐',
    title: 'Open Source',
    description: 'MIT-licensed, extensible, and developer-friendly.'
  },
];

export default function Features() {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800 flex flex-col items-center pb-16">
      <Navbar />
      {/* Animated blurred gradient accent */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[70vw] h-[30vh] bg-gradient-to-tr from-purple-500/30 via-blue-400/20 to-fuchsia-400/20 rounded-full blur-3xl opacity-60 pointer-events-none animate-pulse z-0" />
      <section className="pt-24 pb-10 text-center z-10 relative">
        <h2 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-fuchsia-400 mb-6 drop-shadow-lg tracking-tight">Features</h2>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto font-light mb-12">Everything you need to build, scale, and manage LLM-powered applications—unified, secure, and open source.</p>
      </section>
      <section className="w-full max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 z-10 relative">
        {features.map((feature) => (
          <div key={feature.title} className="backdrop-blur-lg bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl flex flex-col items-center text-center transition-transform duration-200 hover:scale-[1.03] hover:shadow-3xl">
            <span className="text-5xl mb-4 drop-shadow-lg">{feature.icon}</span>
            <h3 className="text-2xl font-bold text-purple-200 mb-2 tracking-tight">{feature.title}</h3>
            <p className="text-gray-200 text-lg font-light leading-relaxed">{feature.description}</p>
          </div>
        ))}
      </section>
    </div>
  );
} 