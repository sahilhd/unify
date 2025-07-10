#!/bin/bash

# UniLLM Quick Start Script for Self-Hosting
# This script will help you get UniLLM running locally in minutes

set -e

echo "🚀 UniLLM Quick Start for Self-Hosting"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ Python and pip are installed"

# Check if we're in the right directory
if [ ! -f "api_gateway/main_phase2.py" ]; then
    echo "❌ Please run this script from the UniLLM root directory"
    echo "   Expected: ./quick_start.sh"
    echo "   Current: $(pwd)"
    exit 1
fi

echo "✅ Running from UniLLM root directory"

# Set up backend
echo ""
echo "🔧 Setting up backend..."
cd api_gateway

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env_example.txt .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file with your API keys:"
    echo "   nano .env"
    echo ""
    echo "   At minimum, you need:"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - SECRET_KEY (generate with: python3 -c \"import secrets; print(secrets.token_urlsafe(32))\")"
    echo ""
    read -p "Press Enter after you've configured your .env file..."
else
    echo "✅ .env file already exists"
fi

# Create data directory
mkdir -p data

echo ""
echo "🎉 Backend setup complete!"
echo ""

# Ask if user wants to start the server
echo "Would you like to start the UniLLM API server now? (y/n)"
read -p "> " start_server

if [[ $start_server =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting UniLLM API server..."
    echo "   API will be available at: http://localhost:8000"
    echo "   Press Ctrl+C to stop"
    echo ""
    python3 main_phase2.py
else
    echo ""
    echo "📋 To start the server later, run:"
    echo "   cd api_gateway"
    echo "   python3 main_phase2.py"
    echo ""
fi

# Ask if user wants to set up frontend
echo ""
echo "Would you like to set up the frontend dashboard? (y/n)"
read -p "> " setup_frontend

if [[ $setup_frontend =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔧 Setting up frontend..."
    cd ../frontend
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js 16+ first."
        echo "   Visit: https://nodejs.org/"
        exit 1
    fi
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is not installed. Please install npm first."
        exit 1
    fi
    
    echo "✅ Node.js and npm are installed"
    
    # Install dependencies
    echo "📦 Installing Node.js dependencies..."
    npm install
    
    echo ""
    echo "🎉 Frontend setup complete!"
    echo ""
    echo "Would you like to start the frontend development server? (y/n)"
    read -p "> " start_frontend
    
    if [[ $start_frontend =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Starting frontend development server..."
        echo "   Dashboard will be available at: http://localhost:3000"
        echo "   Press Ctrl+C to stop"
        echo ""
        npm start
    else
        echo ""
        echo "📋 To start the frontend later, run:"
        echo "   cd frontend"
        echo "   npm start"
        echo ""
    fi
fi

echo ""
echo "🎉 UniLLM setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Register a user: curl -X POST http://localhost:8000/auth/register"
echo "   2. Get your API key from the dashboard"
echo "   3. Start using UniLLM in your applications!"
echo ""
echo "📖 For more information:"
echo "   - Self-hosting guide: SELF_HOSTING_GUIDE.md"
echo "   - Deployment guide: DEPLOYMENT_GUIDE.md"
echo "   - Main documentation: README.md"
echo "" 