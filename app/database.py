"""
Database Module
Sets up SQLAlchemy and defines database models.
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from app.utils.logger import setup_logger

logger = setup_logger('Database')

DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://username:password@localhost:5432/email_validation_db')

engine = create_engine(DATABASE_URI, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class ValidationResult(Base):
    """
    Database Model for Email Validation Results
    """
    __tablename__ = 'validation_results'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    syntax_valid = Column(Boolean, default=False)
    domain_exists = Column(Boolean, default=False)
    mx_records_valid = Column(Boolean, default=False)
    mx_record_valid = Column(Boolean, default=False)
    smtp_verified = Column(Boolean, default=False)
    smtp_valid = Column(Boolean, default=False)
    disposable = Column(Boolean, default=False)
    disposable_check = Column(Boolean, default=False)
    role_account = Column(Boolean, default=False)
    typo_detected = Column(Boolean, default=False)
    typo_suggestion = Column(String, nullable=True)
    domain_reputation = Column(Float, default=0.0)
    spam_trap = Column(Boolean, default=False)
    catch_all = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0, index=True)
    status = Column(String, default="Invalid", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    """
    Initializes the database by creating all tables.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")