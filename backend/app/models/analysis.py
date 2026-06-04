from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, JSON
from sqlalchemy.sql import func 
from app.db.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    user_name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)

    language = Column(String, nullable=True)
    sentiment_overall = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    bias_detected = Column(Boolean, nullable=True)
    bias_lean = Column(String, nullable=True)
    bias_score = Column(Float, nullable=True)
    bias_explanation = Column(String, nullable=True)
    credibility_score = Column(Float, nullable=True)
    propaganda_techniques = Column(JSON, nullable=True)
    loaded_language = Column(JSON, nullable=True)
    summary = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())