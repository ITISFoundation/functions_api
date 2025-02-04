from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .models import JobStatus

SQLALCHEMY_DATABASE_URL = "sqlite:///./functions_store.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class FunctionDB(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    url = Column(String)
    description = Column(String)
    input_schema = Column(JSON, nullable=True)
    output_schema = Column(JSON, nullable=True)    
    tags = Column(JSON, nullable=True)  

class FunctionJobDB(Base):
    __tablename__ = "function_jobs"

    id = Column(Integer, primary_key=True, index=True)
    functionID = Column(Integer)
    status = Column(SQLAEnum(JobStatus), default=JobStatus.PENDING)
    inputs = Column(JSON)
    outputs = Column(JSON)
    job_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)  # Added field

class FunctionJobCollectionDB(Base):
    """Database model for function job collections"""

    __tablename__ = "function_job_collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    job_ids = Column(JSON)  # Store list of job IDs
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
