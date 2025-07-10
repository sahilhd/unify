import React from 'react';

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
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col items-center py-16 px-4">
      <h2 className="text-4xl font-extrabold mb-8 text-purple-400">Features</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl w-full">
        {features.map((feature) => (
          <div key={feature.title} className="bg-gray-800 rounded-lg p-8 shadow-lg flex flex-col items-center text-center">
            <span className="text-5xl mb-4">{feature.icon}</span>
            <h3 className="text-2xl font-bold text-purple-300 mb-2">{feature.title}</h3>
            <p className="text-gray-300">{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
} 