from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.core.database import Base


class PortfolioSnapshot(Base):

    __tablename__ = "portfolio_snapshots"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id")
    )

    portfolio_health_score = Column(Float)

    total_value = Column(Float)

    risk_level = Column(String)

    diversification_score = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )