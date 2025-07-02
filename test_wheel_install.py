#!/usr/bin/env python3
"""
Test script to verify wheel installation works
"""

import subprocess
import sys
import os
import tempfile
import shutil

def test_wheel_installation():
    """Test installing and using the wheel file"""
    print("🧪 Testing wheel installation...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Created temp directory: {temp_dir}")
        
        # Copy wheel file to temp directory
        wheel_file = "dist/unillm-0.1.0-py3-none-any.whl"
        if not os.path.exists(wheel_file):
            print(f"❌ Wheel file not found: {wheel_file}")
            return False
        
        shutil.copy(wheel_file, temp_dir)
        print(f"✅ Copied wheel file to temp directory")
        
        # Create a test script
        test_script = """
import sys
try:
    from unillm.client import UniLLM
    print("✅ Successfully imported UniLLM")
    
    # Test client creation
    client = UniLLM(
        api_key="test_key",
        base_url="https://test.com"
    )
    print("✅ Successfully created client")
    
    print("🎉 All tests passed!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
"""
        
        with open(os.path.join(temp_dir, "test_import.py"), "w") as f:
            f.write(test_script)
        
        # Install wheel in temp environment
        print("📦 Installing wheel...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            os.path.join(temp_dir, "unillm-0.1.0-py3-none-any.whl")
        ], capture_output=True, text=True, cwd=temp_dir)
        
        if result.returncode != 0:
            print(f"❌ Installation failed: {result.stderr}")
            return False
        
        print("✅ Wheel installed successfully")
        
        # Test import
        print("🔍 Testing import...")
        result = subprocess.run([
            sys.executable, "test_import.py"
        ], capture_output=True, text=True, cwd=temp_dir)
        
        if result.returncode != 0:
            print(f"❌ Import test failed: {result.stderr}")
            return False
        
        print(result.stdout)
        return True

def create_usage_example():
    """Create a usage example for sharing"""
    example_code = '''# UniLLM Client Library Usage Example

# 1. Install the library
# pip install unillm-0.1.0-py3-none-any.whl

# 2. Import and use
from unillm.client import UniLLM

# Create client (point to your deployed API)
client = UniLLM(
    api_key="your_api_key_here",  # Get this from the dashboard
    base_url="https://your-deployed-api.com"  # Your Railway/Render URL
)

# Test OpenAI
response = client.chat(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello from OpenAI!"}]
)
print("OpenAI Response:", response.content)

# Test Anthropic
response = client.chat(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Hello from Anthropic!"}]
)
print("Anthropic Response:", response.content)

# Health check
if client.health_check():
    print("✅ API is healthy!")
else:
    print("❌ API is not responding")
'''
    
    with open("USAGE_EXAMPLE.py", "w") as f:
        f.write(example_code)
    
    print("✅ Created USAGE_EXAMPLE.py")

def main():
    """Main test function"""
    print("🚀 UniLLM Wheel Testing")
    print("=" * 40)
    
    # Test wheel installation
    if test_wheel_installation():
        print("\n🎉 Wheel installation test PASSED!")
    else:
        print("\n❌ Wheel installation test FAILED!")
        return
    
    # Create usage example
    create_usage_example()
    
    print("\n📋 Sharing Instructions:")
    print("1. Share the wheel file: dist/unillm-0.1.0-py3-none-any.whl")
    print("2. Share the usage example: USAGE_EXAMPLE.py")
    print("3. Tell users to install with: pip install unillm-0.1.0-py3-none-any.whl")
    print("4. They'll need your deployed API URL and their own API key")

if __name__ == "__main__":
    main() 