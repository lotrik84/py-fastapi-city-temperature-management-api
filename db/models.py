from sqlalchemy import Column, Integer, String

from db.engine import Base


class DBCity(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(1000), nullable=True)
