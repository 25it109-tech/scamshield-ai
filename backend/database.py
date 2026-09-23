from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scamshield.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ScanHistory(Base):
    __tablename__ = "scan_history"
    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(String, nullable=True)
    input_url = Column(String, nullable=True)
    risk_level = Column(String)
    what = Column(String)
    why = Column(String)
    action = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def save_scan_result(input_text, input_url, risk_level, what, why, action):
    db = SessionLocal()
    try:
        record = ScanHistory(
            input_text=input_text,
            input_url=input_url,
            risk_level=risk_level,
            what=what,
            why=why,
            action=action
        )
        db.add(record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DB save error: {e}")
    finally:
        db.close()