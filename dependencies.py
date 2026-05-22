
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)

# Environment variables
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME', 'propertysearch')

# Validate Mongo URL
if not MONGO_URL:
    raise ValueError("MONGO_URL is not set in environment variables")

# Create client with timeout settings
client = AsyncIOMotorClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000,  # 5 sec timeout
    maxPoolSize=10
)

db = client[DB_NAME]

# Check connection
async def connect_db():
    try:
        await client.admin.command('ping')
        logging.info("✅ MongoDB connected successfully")
    except Exception as e:
        logging.error(f"❌ MongoDB connection failed: {e}")
        raise e

def get_db():
    return db

def close_db():
    client.close()
    logging.info("🔒 MongoDB connection closed")
    