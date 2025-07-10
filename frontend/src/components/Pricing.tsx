import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

export default function Pricing() {
  const navigate = useNavigate();
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800 flex flex-col items-center pb-16">
      <Navbar />
      {/* Animated blurred gradient accent */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[70vw] h-[30vh] bg-gradient-to-tr from-purple-500/30 via-blue-400/20 to-fuchsia-400/20 rounded-full blur-3xl opacity-60 pointer-events-none animate-pulse z-0" />
      <section className="pt-24 pb-10 text-center z-10 relative">
        <h2 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-fuchsia-400 mb-6 drop-shadow-lg tracking-tight">Pricing & Credits</h2>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto font-light mb-12">Simple, transparent, and flexible pricing. Pay only for what you use, or scale with custom plans.</p>
      </section>
      <section className="w-full max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 z-10 relative">
        <div className="backdrop-blur-lg bg-white/5 border border-white/10 rounded-2xl p-10 shadow-2xl flex flex-col items-center text-center">
          <div className="text-4xl font-bold text-purple-300 mb-2">$5</div>
          <div className="text-gray-300 mb-2 text-lg">Starter Pack</div>
          <div className="text-gray-400 text-base mb-4">Enough for thousands of GPT-3.5 calls</div>
          <button className="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-lg font-semibold text-white shadow-xl transition-all duration-200" onClick={() => navigate('/login')}>Get Started</button>
        </div>
        <div className="backdrop-blur-lg bg-white/5 border border-white/10 rounded-2xl p-10 shadow-2xl flex flex-col items-center text-center">
          <div className="text-4xl font-bold text-purple-300 mb-2">Custom</div>
          <div className="text-gray-300 mb-2 text-lg">Scale as you grow</div>
          <div className="text-gray-400 text-base mb-4">Contact us for enterprise pricing</div>
          <button className="px-8 py-3 bg-white/10 hover:bg-white/20 rounded-full text-lg font-semibold text-white shadow-xl border border-white/10 transition-all duration-200" onClick={() => window.open('mailto:support@unillm.com', '_blank')}>Contact Sales</button>
        </div>
      </section>
      <div className="flex flex-col md:flex-row gap-4 justify-center mt-16 z-10 relative">
        <button className="px-10 py-4 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-lg font-semibold text-white shadow-xl transition-all duration-200" onClick={() => navigate('/login')}>Create an Account</button>
      </div>
    </div>
  );
} 