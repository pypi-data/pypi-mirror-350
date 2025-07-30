from sqlalchemy import Column, String
from database import Base

class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(String, primary_key=True, index=True)
    hashed_secret = Column(String, nullable=False)

class Admin(Base):
    __tablename__ = "admins"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
