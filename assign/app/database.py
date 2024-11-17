from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Database URL (adjust this for your setup)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # For SQLite (adjust for other databases)

# Create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class for getting sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database (only if they don't exist)
Base.metadata.create_all(bind=engine)
