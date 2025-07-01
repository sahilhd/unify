# UniLLM Phase 2: Marketplace Architecture

## 🎯 **Phase 2 Goals**
Transform the API gateway into a full marketplace platform with unified billing, user management, and analytics.

## 🏗️ **Core Components**

### 1. **User Management System**
- User registration/login
- API key generation and management
- User profiles and settings
- Role-based access (user, admin)

### 2. **Billing & Usage Tracking**
- Real-time usage monitoring
- Cost calculation per provider
- Credit balance management
- Billing history and invoices
- Usage analytics and reports

### 3. **Rate Limiting & Quotas**
- Per-user rate limits
- Daily/monthly usage quotas
- Provider-specific limits
- Burst protection

### 4. **Web Dashboard**
- User dashboard for usage monitoring
- Admin panel for user management
- Real-time analytics
- API key management interface

### 5. **Enhanced API Gateway**
- Authentication middleware
- Usage tracking middleware
- Rate limiting middleware
- Enhanced error handling

## 📊 **Database Schema**

### Users Table
```sql
users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE,
    password_hash VARCHAR,
    api_key VARCHAR UNIQUE,
    credits DECIMAL,
    rate_limit_per_minute INTEGER,
    daily_quota INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### Usage Table
```sql
usage_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    model VARCHAR,
    provider VARCHAR,
    tokens_used INTEGER,
    cost DECIMAL,
    request_timestamp TIMESTAMP,
    response_time_ms INTEGER
)
```

### Billing Table
```sql
billing_history (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    amount DECIMAL,
    description VARCHAR,
    transaction_type VARCHAR, -- 'credit_purchase', 'usage_charge'
    created_at TIMESTAMP
)
```

## 🔐 **Authentication Flow**

1. **User Registration**: Email/password → Generate API key
2. **API Requests**: Include API key in header `X-API-Key: user_api_key`
3. **Middleware Chain**: Auth → Rate Limit → Usage Track → Route Request
4. **Response**: Include usage info in response headers

## 💰 **Billing Model**

### Cost Structure (per 1K tokens)
- **OpenAI GPT-3.5**: $0.002
- **OpenAI GPT-4**: $0.03
- **Anthropic Claude**: $0.015
- **Gemini Pro**: $0.001
- **Mistral**: $0.007

### Markup Strategy
- Base cost + 20% platform fee
- Volume discounts for high usage
- Enterprise pricing tiers

## 🚀 **Implementation Plan**

### Phase 2A: Core Infrastructure
1. Database setup (PostgreSQL)
2. User authentication system
3. API key management
4. Basic usage tracking

### Phase 2B: Billing & Limits
1. Real-time billing calculation
2. Rate limiting middleware
3. Credit balance management
4. Usage quotas

### Phase 2C: Dashboard & Analytics
1. User dashboard
2. Admin panel
3. Analytics and reporting
4. API documentation

### Phase 2D: Enterprise Features
1. Team management
2. Advanced analytics
3. Custom rate limits
4. White-label options

## 🔧 **Technical Stack**

### Backend
- **FastAPI** (existing)
- **PostgreSQL** (new)
- **SQLAlchemy** (ORM)
- **Alembic** (migrations)
- **Redis** (rate limiting cache)

### Frontend
- **React** + **TypeScript**
- **Tailwind CSS**
- **Chart.js** (analytics)
- **React Query** (data fetching)

### Infrastructure
- **Docker** containerization
- **Nginx** reverse proxy
- **Let's Encrypt** SSL
- **Cloudflare** CDN

## 📈 **Success Metrics**

### Technical Metrics
- API response time < 200ms
- 99.9% uptime
- Zero data loss
- < 1% error rate

### Business Metrics
- User acquisition rate
- Revenue per user
- Provider cost optimization
- Customer satisfaction

## 🎯 **Next Steps**

1. Set up PostgreSQL database
2. Implement user authentication
3. Add API key middleware
4. Create usage tracking
5. Build basic dashboard

Ready to start implementation! 🚀 