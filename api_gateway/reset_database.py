#!/usr/bin/env python3
"""
Reset database and create fresh test user for Phase 2
"""

import os
import uuid
from database import Base, engine, SessionLocal, User
from auth import get_password_hash
from dotenv import load_dotenv

load_dotenv()

def reset_database():
    """Reset the database and create fresh tables"""
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️  Creating fresh tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database reset complete!")

def create_test_user():
    """Create a fresh test user"""
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("⚠️  Test user already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Create new test user
        test_user = User(
            email="test@example.com",
            password_hash=get_password_hash("testpass123"),
            api_key="test-api-key-12345",
            credits=100.0,
            rate_limit_per_minute=100,
            daily_quota=50000,
            is_active=True,
            is_admin=False
        )
        
        db.add(test_user)
        db.commit()
        
        print("✅ Test user created successfully!")
        print(f"   Email: test@example.com")
        print(f"   Password: testpass123")
        print(f"   API Key: test-api-key-12345")
        print(f"   Credits: 100.0")
        
        return test_user
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def main():
    """Main function to reset database and create test user"""
    print("🔄 UniLLM Phase 2 Database Reset")
    print("=" * 50)
    
    # Reset database
    reset_database()
    
    # Create test user
    user = create_test_user()
    
    if user:
        print("\n🎉 Database reset and test user creation completed!")
        print("\n📝 Test Credentials:")
        print("   Email: test@example.com")
        print("   Password: testpass123")
        print("   API Key: test-api-key-12345")
        print("\n🚀 You can now run the Phase 2 tests!")
    else:
        print("\n❌ Failed to create test user!")

if __name__ == "__main__":
    main() 