from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config.config import settings
#from app.models.AbcStudentAccounts import AbcStudentAccounts

# Define global variables
client: AsyncIOMotorClient = None
engine: AIOEngine = None  # Use Odmantic's AIOEngine

async def init_db():
    global client, engine
    client = AsyncIOMotorClient(settings.MONGO_URI)
    
    if settings.MONGO_CA_CERT and settings.MONGO_CLIENT_CERT:
        client.admin.command('ping')

    engine = AIOEngine(client=client, database=settings.MONGO_DB_NAME)  # Initialize Odmantic engine

def get_db():
    """Ensure the database is initialized before returning it"""
    if engine is None:
        raise ValueError("Database is not initialized. Call init_db() first.")
    return engine  # Return the Odmantic engine
