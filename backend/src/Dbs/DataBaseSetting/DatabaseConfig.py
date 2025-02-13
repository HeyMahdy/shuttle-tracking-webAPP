import os
from dotenv import load_dotenv, dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Specify full path to .env file
env_path = 'd:/project-managemen-web-app/backend/.env'

# Load environment variables from the specific path
load_dotenv(dotenv_path=env_path, override=True)

# Get DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")

# Raise error if DATABASE_URL is not set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set")



# Create the database engine
engine = create_async_engine(
    DATABASE_URL,
    pool_recycle=3600,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get async DB session
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session





