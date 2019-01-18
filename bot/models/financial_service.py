import datetime

from sqlalchemy import Column, Integer, String, PickleType, Float, ForeignKey, DateTime
from sqlalchemy.orm import backref, relationship

from bot.models.base import Base


class FinancialService(Base):
    __tablename__ = "financial_services"
    id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("users"))
    category = Column(String)
    title = Column(String)
    description = Column(String)
    photo = Column(PickleType)
    required_credit = Column(Integer)
    required_balance = Column(Float)
    date_time = Column(DateTime)

    def __init__(self, owner_user_id, category, title, description, photo, required_credit, required_balance):
        self.owner_user_id = owner_user_id
        self.category = category
        self.title = title
        self.description = description
        self.photo = photo
        self.required_credit = required_credit
        self.required_balance = required_balance
        self.date_time = datetime.datetime.now()
