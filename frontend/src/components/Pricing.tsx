import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Pricing() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col items-center py-16 px-4">
      <h2 className="text-4xl font-extrabold mb-8 text-purple-400">Pricing & Credits</h2>
      <div className="bg-gray-800 rounded-lg p-8 shadow-lg max-w-2xl w-full mb-8">
        <p className="text-lg text-gray-300 mb-4">UniLLM uses a simple, pay-as-you-go credit system. Purchase credits securely with Stripe and use them across all supported LLM providers.</p>
        <ul className="list-disc list-inside text-gray-300 mb-4">
          <li>Transparent pricing per model (see dashboard for details)</li>
          <li>No monthly minimums or hidden fees</li>
          <li>Track your usage and spending in real time</li>
        </ul>
        <div className="flex flex-col md:flex-row gap-4 mt-6">
          <div className="flex-1 bg-gray-700 rounded p-6 text-center">
            <div className="text-3xl font-bold text-purple-300 mb-2">$5</div>
            <div className="text-gray-300 mb-2">Starter Pack</div>
            <div className="text-gray-400 text-sm mb-4">Enough for thousands of GPT-3.5 calls</div>
            <button className="px-6 py-2 bg-purple-500 hover:bg-purple-600 rounded text-white font-semibold shadow" onClick={() => navigate('/login')}>Get Started</button>
          </div>
          <div className="flex-1 bg-gray-700 rounded p-6 text-center">
            <div className="text-3xl font-bold text-purple-300 mb-2">Custom</div>
            <div className="text-gray-300 mb-2">Scale as you grow</div>
            <div className="text-gray-400 text-sm mb-4">Contact us for enterprise pricing</div>
            <button className="px-6 py-2 bg-gray-600 hover:bg-gray-500 rounded text-white font-semibold shadow" onClick={() => window.open('mailto:support@unillm.com', '_blank')}>Contact Sales</button>
          </div>
        </div>
      </div>
      <button className="mt-8 px-8 py-3 bg-purple-500 hover:bg-purple-600 rounded text-lg font-semibold text-white shadow" onClick={() => navigate('/login')}>Create an Account</button>
    </div>
  );
} 