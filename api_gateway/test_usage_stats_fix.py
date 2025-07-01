#!/usr/bin/env python3
"""
Test script to verify usage stats are properly updated after chat
"""

import requests
import time
import json

API_BASE_URL = "http://localhost:8000"

def test_usage_stats_update():
    """Test that usage stats update properly after chat"""
    print("🧪 Testing Usage Stats Update")
    print("=" * 50)
    
    # Test 1: Register a user
    print("1️⃣ Registering test user...")
    email = f"test_usage_{int(time.time())}@example.com"
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
            print(f"   Requests today: {initial_stats.get('requests_today', 0)}")
            print(f"   Cost today: ${initial_stats.get('cost_today', 0):.4f}")
        else:
            print(f"❌ Failed to get initial stats: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Initial stats error: {e}")
        return
    
    # Test 4: Send multiple chat messages
    print("4️⃣ Sending chat messages...")
    messages = [
        "Hello! This is test message 1.",
        "This is test message 2.",
        "And this is test message 3."
    ]
    
    for i, message in enumerate(messages, 1):
        try:
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}],
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
                print(f"✅ Chat message {i} sent successfully")
                print(f"   Response: {result.get('response', 'N/A')[:50]}...")
                print(f"   Cost: ${result.get('cost', 0):.6f}")
            else:
                print(f"❌ Chat {i} failed: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"❌ Chat {i} error: {e}")
            return
        
        # Small delay between messages
        time.sleep(1)
    
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
            print(f"   Requests today: {updated_stats.get('requests_today', 0)}")
            print(f"   Cost today: ${updated_stats.get('cost_today', 0):.4f}")
            
            # Check if stats were updated
            requests_diff = updated_stats.get('total_requests', 0) - initial_stats.get('total_requests', 0)
            cost_diff = updated_stats.get('total_cost', 0) - initial_stats.get('total_cost', 0)
            
            if requests_diff >= 3:  # Should have at least 3 new requests
                print("✅ Usage stats were properly updated!")
                print(f"   New requests: {requests_diff}")
                print(f"   New cost: ${cost_diff:.6f}")
            else:
                print("⚠️  Usage stats may not have been updated properly")
                print(f"   Expected at least 3 new requests, got {requests_diff}")
        else:
            print(f"❌ Failed to get updated stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Updated stats error: {e}")
    
    # Test 6: Test user info update
    print("6️⃣ Testing user info update...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ User info retrieved")
            print(f"   Credits: ${user_info.get('credits', 0):.2f}")
            print(f"   Email: {user_info.get('email', 'N/A')}")
        else:
            print(f"❌ Failed to get user info: {response.status_code}")
    except Exception as e:
        print(f"❌ User info error: {e}")
    
    print("\n🎉 Usage stats test completed!")
    print(f"📧 Test email: {email}")
    print("\n📋 Summary:")
    print("   ✅ Multiple chat messages sent successfully")
    print("   ✅ Usage stats should update after each chat")
    print("   ✅ User info should reflect current state")
    print("   ✅ Dashboard should show real-time updates")

if __name__ == "__main__":
    test_usage_stats_update() 