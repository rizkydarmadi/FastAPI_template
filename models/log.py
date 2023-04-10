from models import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Logs(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    row_input = Column(Integer, nullable=True)
    created_date = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="log")
