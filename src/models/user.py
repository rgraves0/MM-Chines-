from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)  # Telegram User ID
    username = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=True)
    status = Column(String(20), default="pending")  # pending, approved, active, inactive, banned, rejected, expired
    expires_at = Column(DateTime, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow)
    note = Column(Text, nullable=True)
    banned_reason = Column(Text, nullable=True)
    
    def is_active(self):
        if self.status not in ["approved", "active"]:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            self.status = "expired"
            return False
        return True
