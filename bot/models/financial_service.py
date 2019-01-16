from sqlalchemy import Column, Integer, String, PickleType

from bot.models.base import Base


class FinancialService(Base):
    __tablename__ = "financial_services"
    id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer)
    category = Column(String)
    title = Column(String)
    description = Column(String)
    photo = Column(PickleType)
    required_credit = Column(Integer)

    def __init__(self, owner_user_id, category, title, description, photo, required_credit):
        self.owner_user_id = owner_user_id
        self.category = category
        self.title = title
        self.description = description
        self.photo = photo
        self.required_credit = required_credit
