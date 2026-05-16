from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    owner_name = Column(String, nullable=True)

    holdings = relationship("Holding", back_populates="portfolio")