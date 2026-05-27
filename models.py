from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/lily")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    timezone = Column(String, default="America/Chicago")
    api_keys = Column(JSON, default={})
    enabled_modules = Column(JSON, default={})
    subscription_tier = Column(String, default="free")
    created_at = Column(DateTime, default=datetime.utcnow)

class Memory(Base):
    __tablename__ = "memory"

    memory_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    topic = Column(String)
    summary = Column(Text)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Interaction(Base):
    __tablename__ = "interactions"

    interaction_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    interaction_type = Column(String)
    input_text = Column(Text)
    claude_response = Column(Text)
    tools_called = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

class DashboardState(Base):
    __tablename__ = "dashboard_state"

    user_id = Column(String, primary_key=True)
    last_briefing_time = Column(DateTime, nullable=True)
    inbox_unread_count = Column(Integer, default=0)
    top_5_priorities = Column(JSON, default=[])
    weather_location = Column(String, default="Dallas, TX")
    updated_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
