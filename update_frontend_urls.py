#!/usr/bin/env python3
"""
Script to update hardcoded localhost URLs in frontend components
"""

import os
import re

def update_file(file_path, old_url, new_url):
    """Update hardcoded URLs in a file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace hardcoded localhost URLs
        updated_content = content.replace(old_url, new_url)
        
        if content != updated_content:
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"✅ Updated {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed in {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Update all frontend files"""
    frontend_dir = "frontend/src"
    old_url = "http://localhost:8000"
    new_url = "process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'"
    
    # Files to update
    files_to_update = [
        "components/sections/Chat.tsx",
        "components/sections/Analytics.tsx", 
        "components/sections/Billing.tsx",
        "components/sections/ApiKeys.tsx"
    ]
    
    print("🔄 Updating hardcoded URLs in frontend components...")
    
    updated_count = 0
    for file_path in files_to_update:
        full_path = os.path.join(frontend_dir, file_path)
        if os.path.exists(full_path):
            if update_file(full_path, old_url, new_url):
                updated_count += 1
    
    print(f"\n✅ Updated {updated_count} files")
    print("📝 Note: You'll need to manually update the curl examples in ApiKeys.tsx")

if __name__ == "__main__":
    main() 