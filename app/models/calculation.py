from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)

    first_number = Column(Float, nullable=False)
    second_number = Column(Float, nullable=False)

    operation = Column(String, nullable=False)
    result = Column(Float, nullable=False)

    note = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)