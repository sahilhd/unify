import React from 'react';
import Navbar from './Navbar';

export default function Quickstart() {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800 flex flex-col items-center pb-16">
      <Navbar />
      {/* Animated blurred gradient accent */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[70vw] h-[30vh] bg-gradient-to-tr from-purple-500/30 via-blue-400/20 to-fuchsia-400/20 rounded-full blur-3xl opacity-60 pointer-events-none animate-pulse z-0" />
      <section className="pt-24 pb-10 text-center z-10 relative">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-fuchsia-400 mb-6 drop-shadow-lg tracking-tight">Quickstart</h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto font-light mb-12">Get started with UniLLM in minutes. Unified API, open source, and developer-first.</p>
      </section>
      <div className="max-w-4xl w-full z-10 relative">
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">Get Started</h2>
          <p className="mb-4 text-gray-300">UniLLM provides a unified API and SDK for accessing multiple LLM providers. Get started in minutes with our Python SDK or direct API calls.</p>
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-4 mb-4 shadow-xl">
            <div className="text-sm text-gray-400 mb-2">Python SDK Example</div>
            <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-green-200"><code>{`from unillm import UniLLM\n\nclient = UniLLM(api_key=\"your-api-key\")\n\nresponse = client.chat(\n    model=\"gpt-4\",\n    messages=[{\"role\": \"user\", \"content\": \"Hello!\"}]\n)\nprint(response.content)`}</code></pre>
          </div>
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-4 shadow-xl">
            <div className="text-sm text-gray-400 mb-2">Direct API Example (cURL)</div>
            <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-blue-200"><code>{`curl -X POST https://web-production-70deb.up.railway.app/chat/completions \\\n  -H \"Authorization: Bearer your-api-key\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\n    \"model\": \"gpt-4\",\n    \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}]\n  }'`}</code></pre>
          </div>
        </section>
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">Features</h2>
          <ul className="list-disc list-inside text-gray-300 space-y-1">
            <li>Unified API for OpenAI, Anthropic, Gemini, Mistral, Cohere, and more</li>
            <li>Flexible pay-as-you-go credit system</li>
            <li>Stripe payments and real-time billing</li>
            <li>Usage analytics and dashboard</li>
            <li>Secure authentication (Google OAuth, JWT, API keys)</li>
            <li>Open source and developer-friendly</li>
          </ul>
        </section>
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">Deployment Options: Hosted or Self-Hosted</h2>
          <p className="mb-4 text-gray-300">UniLLM is designed for maximum flexibility. You can:</p>
          <ul className="list-disc list-inside text-gray-300 space-y-1 mb-4">
            <li><span className="font-semibold text-purple-200">Use our managed UniLLM service:</span> Sign up, get an API key, and start using the dashboard and unified API instantly. No setup or maintenance required—just pay for what you use.</li>
            <li><span className="font-semibold text-purple-200">Self-host UniLLM:</span> Deploy the open source platform on your own infrastructure for full privacy, compliance, and custom integrations. Perfect for teams and enterprises with special requirements.</li>
          </ul>
          <p className="text-gray-400 mb-4">Choose the option that fits your needs. Both offer the same powerful features, unified API, and developer experience.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 shadow-xl">
              <h3 className="text-xl font-bold mb-3 text-purple-200">🚀 Quick Self-Hosting</h3>
              <p className="text-gray-300 mb-4">Get your own instance running in 5 minutes:</p>
              <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-green-200 mb-4"><code>{`# Clone and setup
git clone https://github.com/yourusername/unillm
cd unillm
./quick_start.sh

# Or manually:
cd api_gateway
pip install -r requirements.txt
cp env_example.txt .env
# Edit .env with your API keys
python main_phase2.py`}</code></pre>
              <p className="text-gray-400 text-sm">Your API will be available at <code className="text-purple-300">http://localhost:8000</code></p>
            </div>
            
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 shadow-xl">
              <h3 className="text-xl font-bold mb-3 text-purple-200">🐳 Docker Deployment</h3>
              <p className="text-gray-300 mb-4">Production-ready deployment with Docker:</p>
              <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-green-200 mb-4"><code>{`# Create .env file
cp env_example.txt .env
# Edit with your API keys

# Deploy with Docker Compose
docker-compose up -d`}</code></pre>
              <p className="text-gray-400 text-sm">Includes API, frontend, and nginx reverse proxy</p>
            </div>
          </div>
          
          <div className="mt-6 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/30 rounded-2xl p-6">
            <h3 className="text-lg font-bold mb-2 text-purple-200">🧪 Test Your Setup</h3>
            <p className="text-gray-300 mb-3">Verify your self-hosted instance is working:</p>
            <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-green-200"><code>{`# Test your instance
python test_self_hosted.py

# Or test a specific URL
python test_self_hosted.py https://your-domain.com`}</code></pre>
          </div>
        </section>
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">API Reference</h2>
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-4 mb-4 shadow-xl">
            <div className="text-sm text-gray-400 mb-2">POST /chat/completions</div>
            <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-blue-200"><code>{`{\n  \"model\": \"gpt-4\",\n  \"messages\": [\n    {\"role\": \"user\", \"content\": \"Say hello!\"}\n  ],\n  \"temperature\": 0.7,\n  \"max_tokens\": 1000\n}`}</code></pre>
          </div>
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-4 mb-4 shadow-xl">
            <div className="text-sm text-gray-400 mb-2">Authentication</div>
            <pre className="bg-gray-900/80 rounded p-3 overflow-x-auto text-sm text-blue-200"><code>{`Authorization: Bearer your-api-key`}</code></pre>
          </div>
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-4 shadow-xl">
            <div className="text-sm text-gray-400 mb-2">Other Endpoints</div>
            <ul className="list-disc list-inside text-gray-300">
              <li><span className="font-mono">/auth/register</span> - Register a new user</li>
              <li><span className="font-mono">/auth/login</span> - Login and get API key</li>
              <li><span className="font-mono">/billing/purchase-credits</span> - Buy credits</li>
              <li><span className="font-mono">/billing/usage</span> - Get usage stats</li>
              <li><span className="font-mono">/models</span> - List available models</li>
            </ul>
          </div>
        </section>
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">Use Cases</h2>
          <ul className="list-disc list-inside text-gray-300 space-y-1">
            <li>Build chatbots and assistants with any LLM provider</li>
            <li>Integrate LLMs into your SaaS or internal tools</li>
            <li>Experiment with multiple models using a single SDK</li>
            <li>Track and manage LLM usage and costs for your team</li>
          </ul>
        </section>
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">FAQ</h2>
          <ul className="list-disc list-inside text-gray-300 space-y-1">
            <li><span className="font-semibold text-purple-200">How do I get an API key?</span> Register for an account and your API key will be available in the dashboard.</li>
            <li><span className="font-semibold text-purple-200">How is billing handled?</span> Purchase credits with Stripe and use them across all models. See the Pricing page for details.</li>
            <li><span className="font-semibold text-purple-200">Is UniLLM open source?</span> Yes! <a href="https://github.com/sahilhd/unify" target="_blank" rel="noopener noreferrer" className="underline text-purple-300">View on GitHub</a></li>
            <li><span className="font-semibold text-purple-200">Where can I get support?</span> Open an issue on GitHub or email support@unillm.com</li>
          </ul>
        </section>
        <div className="flex flex-col md:flex-row gap-4 justify-center mt-8">
          <a href="/pricing" className="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 rounded-full text-lg font-semibold text-white shadow-xl transition-all duration-200 text-center">See Pricing</a>
          <a href="https://github.com/sahilhd/unify" target="_blank" rel="noopener noreferrer" className="px-8 py-3 bg-white/10 hover:bg-white/20 rounded-full text-lg font-semibold text-white shadow-xl border border-white/10 transition-all duration-200 text-center">View on GitHub</a>
        </div>
      </div>
    </div>
  );
} 