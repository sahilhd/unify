#!/usr/bin/env python3
"""
Script to properly fix hardcoded URLs in frontend components
"""

import os
import re

def fix_file(file_path):
    """Fix URLs in a file with proper template literals"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Fix the incorrectly replaced URLs
        # Replace the broken pattern with proper template literal
        old_pattern = r"'process\.env\.REACT_APP_API_BASE_URL \|\| 'http://localhost:8000'"
        new_pattern = r"`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}"
        
        updated_content = re.sub(old_pattern, new_pattern, content)
        
        # Also fix any remaining hardcoded localhost URLs
        updated_content = updated_content.replace(
            "http://localhost:8000", 
            "${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}"
        )
        
        if content != updated_content:
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"✅ Fixed {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed in {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all frontend files"""
    frontend_dir = "frontend/src"
    
    # Files to fix
    files_to_fix = [
        "components/sections/Chat.tsx",
        "components/sections/Analytics.tsx", 
        "components/sections/Billing.tsx",
        "components/sections/ApiKeys.tsx"
    ]
    
    print("🔄 Fixing URLs in frontend components...")
    
    fixed_count = 0
    for file_path in files_to_fix:
        full_path = os.path.join(frontend_dir, file_path)
        if os.path.exists(full_path):
            if fix_file(full_path):
                fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main() 