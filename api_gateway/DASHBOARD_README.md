# UniLLM Dashboard & Analytics

This directory contains the web dashboard and analytics system for the UniLLM marketplace.

## 🚀 Quick Start

### 1. Start the UniLLM Server
```bash
# Make sure the server is running
python main_phase2.py
```

### 2. Launch the Dashboard
```bash
# Install dependencies and launch dashboard
python launch_dashboard.py
```

The dashboard will be available at: http://localhost:8501

## 📊 Features

### Web Dashboard (`dashboard.py`)
- **User Authentication**: Register, login, and manage accounts
- **Chat Interface**: Send messages to any supported model
- **Model Selection**: Choose from all available providers and models
- **Usage Statistics**: Real-time usage tracking and cost monitoring
- **Credit Management**: Purchase and manage credits
- **Provider Switching**: Seamlessly switch between different LLM providers

### Analytics System (`analytics.py`)
- **Usage Analytics**: Detailed usage patterns and trends
- **Provider Performance**: Success rates, response times, and cost analysis
- **User Analytics**: Individual user usage statistics
- **Model Analytics**: Performance metrics for each model
- **Daily Trends**: Time-series analysis of usage patterns

## 🛠️ Installation

### Dependencies
```bash
pip install -r requirements_dashboard.txt
```

### Required Packages
- `streamlit`: Web application framework
- `plotly`: Interactive charts and visualizations
- `pandas`: Data manipulation and analysis
- `requests`: HTTP client for API communication

## 📈 Usage

### Dashboard Features

#### 1. Authentication
- Register a new account or login with existing credentials
- Each user gets a unique API key for programmatic access

#### 2. Chat Interface
- Select provider (OpenAI, Anthropic, Google, etc.)
- Choose specific model (GPT-4, Claude-3-sonnet, etc.)
- Adjust temperature and max tokens
- Send messages and get AI responses

#### 3. Usage Monitoring
- Real-time usage statistics
- Cost tracking and billing history
- Credit balance and purchase options

#### 4. Model Information
- Complete list of available models
- Provider-specific model details
- Performance characteristics

### Analytics Features

#### 1. System Analytics
- Overall platform usage statistics
- Provider performance comparison
- Cost distribution analysis
- User activity patterns

#### 2. User Analytics
- Individual usage tracking
- Personal cost analysis
- Request history and patterns

#### 3. Provider Analytics
- Success rates by provider
- Response time analysis
- Cost efficiency metrics

## 🔧 Configuration

### Environment Variables
Make sure your `.env` file contains the necessary API keys:
```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_gemini_key
MISTRAL_API_KEY=your_mistral_key
COHERE_API_KEY=your_cohere_key
```

### Dashboard Configuration
The dashboard connects to the UniLLM server at `http://localhost:8000` by default.
You can modify this in the `dashboard.py` file if needed.

## 📱 API Integration

The dashboard uses the same API endpoints as the main UniLLM server:

- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /auth/me` - Get user information
- `POST /chat/completions` - Send chat messages
- `GET /billing/usage` - Get usage statistics
- `POST /billing/purchase-credits` - Purchase credits

## 🎯 Use Cases

### 1. Development & Testing
- Test different models and providers
- Compare response quality and performance
- Debug API integration issues

### 2. Business Analytics
- Monitor platform usage and costs
- Analyze user behavior patterns
- Optimize provider selection

### 3. User Management
- Track individual user usage
- Manage credit allocations
- Monitor system performance

## 🔒 Security

- All API communications use HTTPS (in production)
- User authentication with JWT tokens
- API key-based access control
- Rate limiting and usage quotas

## 🚀 Deployment

### Local Development
```bash
# Terminal 1: Start the server
python main_phase2.py

# Terminal 2: Launch dashboard
python launch_dashboard.py
```

### Production Deployment
1. Set up a production database (PostgreSQL/MySQL)
2. Configure environment variables
3. Set up SSL/TLS certificates
4. Deploy with a production WSGI server
5. Configure reverse proxy (nginx/Apache)

## 📝 Troubleshooting

### Common Issues

1. **Dashboard won't start**
   - Check if the UniLLM server is running
   - Verify all dependencies are installed
   - Check port 8501 is available

2. **Authentication errors**
   - Verify API keys are correctly set
   - Check server logs for errors
   - Ensure database is properly initialized

3. **No data in analytics**
   - Make sure usage tracking is enabled
   - Check database permissions
   - Verify API endpoints are working

### Logs
- Server logs: `server_phase2.log`
- Dashboard logs: Check Streamlit output
- Database: `unillm.db`

## 🤝 Contributing

To add new features to the dashboard:

1. Modify `dashboard.py` for UI changes
2. Update `analytics.py` for new analytics
3. Add new API endpoints if needed
4. Update documentation

## 📄 License

This project is part of the UniLLM marketplace system. 