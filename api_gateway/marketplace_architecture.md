# UniLLM Marketplace Architecture

## 🎯 Vision: Unified LLM Marketplace with Single Billing

Transform our API gateway into a platform where developers:
- Pay once, access all providers
- Get unified billing and credit system
- Enjoy seamless provider switching
- Access benchmarking and cost optimization

## 🏗️ Current Architecture vs. Marketplace Needs

### Current State (API Gateway)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │───▶│  API Gateway    │───▶│  LLM Providers  │
│                 │    │  (FastAPI)      │    │  (OpenAI, etc.) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Target State (Marketplace)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │───▶│  Marketplace    │───▶│  LLM Providers  │
│   (Dashboard)   │    │  Backend        │    │  (OpenAI, etc.) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Billing System │
                       │  (Stripe, etc.) │
                       └─────────────────┘
```

## 🔧 Required Components

### 1. User Management & Authentication
```python
# New modules needed:
- auth/ - User registration, login, JWT tokens
- users/ - User profiles, preferences, settings
- organizations/ - Team management, billing groups
```

### 2. Billing & Credit System
```python
# New modules needed:
- billing/ - Credit management, usage tracking
- payments/ - Stripe integration, subscription management
- usage/ - Token counting, cost calculation
- pricing/ - Provider pricing, markup, discounts
```

### 3. Advanced API Features
```python
# Enhanced modules:
- routing/ - Smart routing, load balancing, fallbacks
- analytics/ - Usage metrics, performance tracking
- benchmarking/ - Model comparison, performance testing
- caching/ - Response caching, cost optimization
```

### 4. Frontend Dashboard
```python
# New frontend needed:
- React/Vue.js dashboard
- Credit management interface
- Usage analytics and reports
- Model comparison tools
- Developer documentation
```

## 📊 Database Schema

### Users & Organizations
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    credits DECIMAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Organizations table
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    billing_email VARCHAR,
    credits DECIMAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Usage Tracking
```sql
-- Usage tracking table
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    model VARCHAR NOT NULL,
    provider VARCHAR NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost DECIMAL,
    response_time INTEGER,
    success BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Billing & Payments
```sql
-- Billing table
CREATE TABLE billing_events (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    event_type VARCHAR NOT NULL, -- 'credit_purchase', 'usage_charge'
    amount DECIMAL NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔄 API Enhancements

### Enhanced Chat Endpoint
```python
@app.post("/chat/completions")
async def chat_completions(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)  # NEW: Auth
):
    # NEW: Check credits
    if not has_sufficient_credits(current_user, request.model):
        raise HTTPException(400, "Insufficient credits")
    
    # NEW: Track usage
    start_time = time.time()
    
    try:
        # Get provider and make request
        provider = get_provider_for_model(request.model)
        adapter = get_adapter(provider)
        response = adapter.chat(request)
        
        # NEW: Calculate and deduct cost
        cost = calculate_cost(request.model, response.usage)
        deduct_credits(current_user, cost)
        
        # NEW: Log usage
        log_usage(current_user, request.model, provider, response.usage, cost, time.time() - start_time)
        
        return response
        
    except Exception as e:
        # NEW: Log failed request
        log_failed_request(current_user, request.model, str(e))
        raise
```

### New Endpoints Needed
```python
# User management
@app.post("/auth/register")
@app.post("/auth/login")
@app.get("/auth/me")

# Credit management
@app.get("/credits/balance")
@app.post("/credits/purchase")
@app.get("/credits/history")

# Usage analytics
@app.get("/analytics/usage")
@app.get("/analytics/costs")
@app.get("/analytics/models")

# Model information
@app.get("/models/pricing")
@app.get("/models/benchmarks")
@app.get("/models/recommendations")
```

## 💰 Pricing Strategy

### Cost Structure
```python
# Provider costs (example)
PROVIDER_COSTS = {
    "openai": {
        "gpt-4": {"input": 0.03, "output": 0.06},  # per 1K tokens
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
    },
    "anthropic": {
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015}
    }
}

# Marketplace markup (example)
MARKUP_PERCENTAGE = 0.10  # 10% markup
```

### Credit System
```python
# Credit conversion
CREDIT_TO_USD = 1.0  # 1 credit = $1 USD

# Example pricing
def calculate_cost(model: str, usage: TokenUsage) -> float:
    provider = get_provider_for_model(model)
    costs = PROVIDER_COSTS[provider][model]
    
    total_cost = (
        (usage.prompt_tokens / 1000) * costs["input"] +
        (usage.completion_tokens / 1000) * costs["output"]
    )
    
    # Apply markup
    return total_cost * (1 + MARKUP_PERCENTAGE)
```

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Current)
- ✅ Basic API gateway
- ✅ Provider adapters
- ✅ Unified interface

### Phase 2: Billing & Auth
- 🔄 User authentication
- 🔄 Credit system
- 🔄 Usage tracking
- 🔄 Basic billing

### Phase 3: Advanced Features
- 📋 Model benchmarking
- 📋 Smart routing
- 📋 Fallback mechanisms
- 📋 Usage analytics

### Phase 4: Frontend & UX
- 📋 Web dashboard
- 📋 Developer portal
- 📋 Documentation
- 📋 SDKs

### Phase 5: Enterprise Features
- 📋 Team management
- 📋 Advanced analytics
- 📋 Custom pricing
- 📋 White-label solutions

## 💡 Competitive Advantages

### vs. OpenRouter
- Better UX and developer experience
- Unified credit system (no separate provider accounts)
- Advanced analytics and cost optimization
- Custom pricing and enterprise features

### vs. Together.ai
- Focus on commercial models (not just open source)
- Better provider coverage
- More advanced routing and fallback
- Comprehensive billing and analytics

## 🎯 Next Steps

1. **Start with Phase 2** - Add authentication and basic billing
2. **Build MVP dashboard** - Simple credit management and usage tracking
3. **Test with real users** - Get feedback on pricing and features
4. **Iterate and scale** - Add advanced features based on user needs

The current API gateway provides an excellent foundation, but we need significant additions to create a true marketplace platform. 