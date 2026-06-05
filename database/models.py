"""
Database models for OpsCore Lead Generation Engine
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Company(Base):
    """Company model"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    property_name = Column(String(255))
    property_type = Column(String(100))
    city = Column(String(100))
    country = Column(String(100), index=True)
    website = Column(String(255))
    linkedin_company = Column(String(255))
    num_locations = Column(Integer, default=1)
    priority_score = Column(Integer, default=0)
    tier = Column(String(50))
    source_url = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    decision_makers = relationship("DecisionMaker", back_populates="company")
    contact_history = relationship("ContactHistory", back_populates="company")
    
    def __repr__(self):
        return f"<Company {self.name}>"


class DecisionMaker(Base):
    """Decision maker model"""
    __tablename__ = "decision_makers"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    title = Column(String(255))
    email = Column(String(255), index=True)
    phone = Column(String(20))
    linkedin_url = Column(String(500))
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="decision_makers")
    outreach_messages = relationship("OutreachMessage", back_populates="decision_maker")
    
    def __repr__(self):
        return f"<DecisionMaker {self.name} at {self.company_id}>"


class OutreachMessage(Base):
    """Outreach message model"""
    __tablename__ = "outreach_messages"
    
    id = Column(Integer, primary_key=True)
    decision_maker_id = Column(Integer, ForeignKey("decision_makers.id"), nullable=False)
    message_type = Column(String(50))  # linkedin, email, sms
    content = Column(Text)
    sent_at = Column(DateTime)
    status = Column(String(50), default="pending")  # pending, sent, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    decision_maker = relationship("DecisionMaker", back_populates="outreach_messages")
    
    def __repr__(self):
        return f"<OutreachMessage {self.message_type} to {self.decision_maker_id}>"


class ContactHistory(Base):
    """Contact history and response tracking"""
    __tablename__ = "contact_history"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    contact_type = Column(String(50))  # linkedin, email, phone
    status = Column(String(50))  # not_contacted, contacted, interested, meeting_scheduled, opportunity
    response = Column(Text)
    meeting_scheduled = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="contact_history")
    
    def __repr__(self):
        return f"<ContactHistory {self.company_id} - {self.status}>"
