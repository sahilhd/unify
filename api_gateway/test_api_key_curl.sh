#!/bin/bash

# UniLLM API Key Test - Curl Version
# Use this script to test your UniLLM API key with curl commands

echo "🚀 UniLLM API Key Test - Curl Version"
echo "======================================"

# Get API key from user
echo ""
echo "📋 Instructions:"
echo "1. Copy your UniLLM API key (starts with 'unillm_')"
echo "2. Paste it below when prompted"
echo "3. Make sure your UniLLM server is running on localhost:8000"
echo ""
echo "----------------------------------------"

read -p "🔑 Enter your UniLLM API key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ No API key provided!"
    exit 1
fi

if [[ ! $API_KEY == unillm_* ]]; then
    echo "❌ Invalid API key format! Should start with 'unillm_'"
    exit 1
fi

read -p "🌐 Enter server URL (default: http://localhost:8000): " SERVER_URL
if [ -z "$SERVER_URL" ]; then
    SERVER_URL="http://localhost:8000"
fi

echo ""
echo "🚀 Starting test with key: ${API_KEY:0:20}..."
echo "🌐 Server: $SERVER_URL"
echo ""

# Test 1: Health Check
echo "1️⃣ Testing server health..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$SERVER_URL/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Server is healthy!"
    echo "   Response: $RESPONSE_BODY"
else
    echo "❌ Server health check failed: $HTTP_CODE"
    echo "   Response: $RESPONSE_BODY"
    exit 1
fi

echo ""

# Test 2: Chat Completion
echo "2️⃣ Testing chat completion..."
CHAT_RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST "$SERVER_URL/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say \"Hello from UniLLM!\" in exactly 5 words."}
        ],
        "max_tokens": 20
    }')

HTTP_CODE=$(echo "$CHAT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$CHAT_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Chat completion successful!"
    echo "   Response: $RESPONSE_BODY"
else
    echo "❌ Chat completion failed: $HTTP_CODE"
    echo "   Response: $RESPONSE_BODY"
    exit 1
fi

echo ""

# Test 3: Usage Stats
echo "3️⃣ Testing usage stats..."
USAGE_RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "Authorization: Bearer $API_KEY" \
    "$SERVER_URL/billing/usage")

HTTP_CODE=$(echo "$USAGE_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$USAGE_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Usage stats retrieved!"
    echo "   Response: $RESPONSE_BODY"
else
    echo "❌ Usage stats failed: $HTTP_CODE"
    echo "   Response: $RESPONSE_BODY"
fi

echo ""
echo "======================================"
echo "🎉 API Key test completed!"
echo ""
echo "✅ Your API key is working correctly!"
echo "💡 You can now use this API key in your applications."
echo ""
echo "📝 Example usage:"
echo "curl -X POST $SERVER_URL/chat/completions \\"
echo "  -H \"Authorization: Bearer $API_KEY\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"model\": \"gpt-3.5-turbo\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}]}'" 