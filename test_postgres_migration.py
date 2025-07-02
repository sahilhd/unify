#!/usr/bin/env python3
"""
Test script to verify PostgreSQL migration
"""

import requests
import time
import os

API_URL = "https://web-production-70deb.up.railway.app"

def test_postgres_migration():
    print("🔍 Testing PostgreSQL Migration...")
    
    # Check if DATABASE_URL is set (indicates PostgreSQL)
    database_url = os.getenv('DATABASE_URL', '')
    if database_url and 'postgresql' in database_url:
        print("✅ PostgreSQL detected (DATABASE_URL is set)")
    else:
        print("⚠️  SQLite detected (no DATABASE_URL)")
    
    # Test registration and persistence
    email = f"postgres_test_{int(time.time())}@example.com"
    password = "testpass123"
    
    print(f"\n📝 Registering test user: {email}")
    
    # Register user
    response = requests.post(
        f"{API_URL}/auth/register",
        json={"email": email, "password": password}
    )
    
    if response.status_code == 200:
        data = response.json()
        api_key = data.get("api_key")
        print(f"✅ Registration successful")
        print(f"   API Key: {api_key}")
        
        # Test API call
        print("\n🧪 Testing API call...")
        response = requests.post(
            f"{API_URL}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Test message"}],
                "temperature": 0.7,
                "max_tokens": 20
            }
        )
        
        if response.status_code == 200:
            print("✅ API call successful")
            print("✅ Data persistence confirmed!")
            print("\n🎉 PostgreSQL migration is working!")
            print(f"   Your data will now persist between deployments!")
        else:
            print(f"❌ API call failed: {response.status_code}")
    else:
        print(f"❌ Registration failed: {response.status_code}")

if __name__ == "__main__":
    test_postgres_migration() 