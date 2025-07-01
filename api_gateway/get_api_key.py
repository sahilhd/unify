#!/usr/bin/env python3
"""
Get UniLLM API Key
Simple script to retrieve your API key by logging in
"""

import requests
import sys

def get_api_key(email, password, base_url="http://localhost:8000"):
    """
    Get API key by logging in with email and password
    
    Args:
        email: User email
        password: User password
        base_url: UniLLM server URL
    
    Returns:
        API key if successful, None otherwise
    """
    
    try:
        # First try to login
        response = requests.post(
            f"{base_url}/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            api_key = data['user']['api_key']
            credits = data['user']['credits']
            print(f"✅ Login successful!")
            print(f"📧 Email: {email}")
            print(f"💰 Credits: ${credits}")
            print(f"🔑 API Key: {api_key}")
            return api_key
        else:
            print(f"❌ Login failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def register_and_get_key(email, password, base_url="http://localhost:8000"):
    """
    Register a new user and get their API key
    
    Args:
        email: User email
        password: User password
        base_url: UniLLM server URL
    
    Returns:
        API key if successful, None otherwise
    """
    
    try:
        # Register new user
        response = requests.post(
            f"{base_url}/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            api_key = data['api_key']
            credits = data['credits']
            print(f"✅ Registration successful!")
            print(f"📧 Email: {email}")
            print(f"💰 Credits: ${credits}")
            print(f"🔑 API Key: {api_key}")
            return api_key
        else:
            print(f"❌ Registration failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def main():
    """Main function"""
    print("🔑 UniLLM API Key Getter")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ UniLLM server is not running!")
            print("💡 Start the server with: python main_phase2.py")
            return
    except:
        print("❌ Cannot connect to UniLLM server!")
        print("💡 Make sure the server is running on localhost:8000")
        return
    
    print("✅ Server is running!")
    print()
    
    # Get user input
    email = input("📧 Enter your email: ").strip()
    password = input("🔒 Enter your password: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required!")
        return
    
    print()
    print("🔄 Attempting to login...")
    
    # Try to login first
    api_key = get_api_key(email, password)
    
    if api_key is None:
        print()
        print("❌ Login failed. Would you like to register a new account?")
        register_choice = input("Register new account? (y/n): ").strip().lower()
        
        if register_choice in ['y', 'yes']:
            print()
            print("🔄 Registering new account...")
            api_key = register_and_get_key(email, password)
        else:
            print("👋 Goodbye!")
            return
    
    if api_key:
        print()
        print("🎉 Success! You can now use this API key in your applications.")
        print()
        print("📝 Example usage:")
        print(f"curl -X POST http://localhost:8000/chat/completions \\")
        print(f"  -H \"Authorization: Bearer {api_key}\" \\")
        print(f"  -H \"Content-Type: application/json\" \\")
        print(f"  -d '{{\"model\": \"gpt-3.5-turbo\", \"messages\": [{{\"role\": \"user\", \"content\": \"Hello!\"}}]}}'")

if __name__ == "__main__":
    main() 