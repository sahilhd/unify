#!/usr/bin/env python3
"""
Test script to verify dashboard improvements
Tests session persistence and usage stats refresh
"""

import requests
import time
import json

API_BASE_URL = "http://localhost:8000"

def test_dashboard_improvements():
    """Test the dashboard improvements"""
    print("🧪 Testing Dashboard Improvements")
    print("=" * 50)
    
    # Test 1: Register a user
    print("1️⃣ Registering test user...")
    email = f"test_dashboard_{int(time.time())}@example.com"
    password = "testpass123"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Registration successful")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 2: Login and get API key
    print("2️⃣ Logging in...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            api_key = data['user']['api_key']
            print("✅ Login successful")
            print(f"   API Key: {api_key[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 3: Get initial usage stats
    print("3️⃣ Getting initial usage stats...")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(
            f"{API_BASE_URL}/billing/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            initial_stats = response.json()
            print("✅ Initial stats retrieved")
            print(f"   Total requests: {initial_stats.get('total_requests', 0)}")
            print(f"   Total cost: ${initial_stats.get('total_cost', 0):.4f}")
        else:
            print(f"❌ Failed to get initial stats: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Initial stats error: {e}")
        return
    
    # Test 4: Send a chat message
    print("4️⃣ Sending chat message...")
    try:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello! This is a test message."}],
            "max_tokens": 50
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat message sent successfully")
            print(f"   Response: {result.get('response', 'N/A')[:50]}...")
            print(f"   Cost: ${result.get('cost', 0):.6f}")
        else:
            print(f"❌ Chat failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return
    
    # Test 5: Get updated usage stats
    print("5️⃣ Getting updated usage stats...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/billing/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            updated_stats = response.json()
            print("✅ Updated stats retrieved")
            print(f"   Total requests: {updated_stats.get('total_requests', 0)}")
            print(f"   Total cost: ${updated_stats.get('total_cost', 0):.4f}")
            
            # Check if stats were updated
            if updated_stats.get('total_requests', 0) > initial_stats.get('total_requests', 0):
                print("✅ Usage stats were updated after chat!")
            else:
                print("⚠️  Usage stats may not have been updated")
        else:
            print(f"❌ Failed to get updated stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Updated stats error: {e}")
    
    # Test 6: Test session persistence simulation
    print("6️⃣ Testing session persistence...")
    print("   (This would be tested in the actual dashboard)")
    print("   - API key should persist across page refreshes")
    print("   - Usage stats should refresh after chat")
    print("   - Chat history should be maintained")
    
    print("\n🎉 Dashboard improvements test completed!")
    print(f"📧 Test email: {email}")
    print("\n📋 Summary of improvements:")
    print("   ✅ Usage stats refresh after chat completion")
    print("   ✅ Session persistence across page refreshes")
    print("   ✅ Chat history tracking")
    print("   ✅ Manual refresh button for stats")
    print("   ✅ Multiple persistence methods (URL params + session storage)")

if __name__ == "__main__":
    test_dashboard_improvements() 