import datetime

from sqlalchemy import Column, Integer, String, PickleType, Float, DateTime, Text

from bot.models.base import Base


class FinancialService(Base):
    __tablename__ = "financial_services"
    id = Column(Integer, primary_key=True)
    owner_national_id = Column(String(10))
    category = Column(String(40))
    title = Column(String(40))
    description = Column(Text)
    photo = Column(PickleType)
    required_credit = Column(Integer)
    required_balance = Column(Float)
    date_time = Column(DateTime)

    def __init__(self, owner_user_id, category, title, description, required_credit, required_balance, photo=None):
        self.owner_user_id = owner_user_id
        self.category = category
        self.title = title
        self.description = description
        self.photo = photo
        self.required_credit = required_credit
        self.required_balance = required_balance
        self.date_time = datetime.datetime.now()
