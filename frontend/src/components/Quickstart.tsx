import React from 'react';
import Navbar from './Navbar';

export default function Quickstart() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col items-center py-12 px-4">
      <Navbar />
      <div className="max-w-4xl w-full">
        <h1 className="text-4xl font-extrabold mb-6 text-purple-400 text-center">Quickstart</h1>
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">Get Started</h2>
          <p className="mb-4 text-gray-300">UniLLM provides a unified API and SDK for accessing multiple LLM providers. Get started in minutes with our Python SDK or direct API calls.</p>
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <div className="text-sm text-gray-400 mb-2">Python SDK Example</div>
            <pre className="bg-gray-900 rounded p-3 overflow-x-auto text-sm text-green-200"><code>{`from unillm import UniLLM

client = UniLLM(api_key="your-api-key")

response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content)`}</code></pre>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-2">Direct API Example (cURL)</div>
            <pre className="bg-gray-900 rounded p-3 overflow-x-auto text-sm text-blue-200"><code>{`curl -X POST https://web-production-70deb.up.railway.app/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'`}</code></pre>
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
          <p className="text-gray-400">Choose the option that fits your needs. Both offer the same powerful features, unified API, and developer experience.</p>
        </section>

        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-2 text-purple-300">API Reference</h2>
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <div className="text-sm text-gray-400 mb-2">POST /chat/completions</div>
            <pre className="bg-gray-900 rounded p-3 overflow-x-auto text-sm text-blue-200"><code>{`{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Say hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}`}</code></pre>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <div className="text-sm text-gray-400 mb-2">Authentication</div>
            <pre className="bg-gray-900 rounded p-3 overflow-x-auto text-sm text-blue-200"><code>{`Authorization: Bearer your-api-key`}</code></pre>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
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
          <a href="/pricing" className="px-8 py-3 bg-purple-500 hover:bg-purple-600 rounded text-lg font-semibold text-white shadow text-center">See Pricing</a>
          <a href="https://github.com/sahilhd/unify" target="_blank" rel="noopener noreferrer" className="px-8 py-3 bg-gray-700 hover:bg-gray-600 rounded text-lg font-semibold text-white shadow text-center">View on GitHub</a>
        </div>
      </div>
    </div>
  );
} 