# Database Migration Guide

## 🚨 Current Issue
Railway's ephemeral storage wipes your SQLite database on every redeploy, losing all users and data.

## 💡 Solution: Migrate to PostgreSQL

### Step 1: Add PostgreSQL to Railway
1. Go to your Railway project dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Railway will provide connection details

### Step 2: Update Backend Code
Replace SQLite with PostgreSQL in your backend:

```python
# Install PostgreSQL driver
pip install psycopg2-binary

# Update database.py
import psycopg2
from psycopg2.extras import RealDictCursor

# Use DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
```

### Step 3: Update Requirements
Add to `requirements.txt`:
```
psycopg2-binary==2.9.7
```

### Step 4: Environment Variables
Railway will automatically set:
- `DATABASE_URL`: PostgreSQL connection string

## 🔄 Alternative: Keep SQLite with Volume Mount
If you prefer SQLite, you can mount a persistent volume, but PostgreSQL is recommended for production.

## 📊 Benefits of PostgreSQL
- ✅ Data persists between deployments
- ✅ Better performance for multiple users
- ✅ Built-in backup and recovery
- ✅ Railway managed (no maintenance needed)

## 🚀 Quick Migration Steps
1. Add PostgreSQL plugin in Railway
2. Update backend code to use PostgreSQL
3. Deploy updated code
4. Data will persist forever! 