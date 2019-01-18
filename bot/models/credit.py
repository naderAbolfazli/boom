from sqlalchemy import Column, Integer, String, ForeignKey, Float

from bot.models.base import Base


class Credit(Base):
    __tablename__ = "credit"
    id = Column(Integer, primary_key=True)
    from_user = Column(Integer)
    to_user = Column(Integer)
    balance = Column(Float)

    def __init__(self, from_user,to_user,balance):
        self.from_user = from_user
        self.to_user = to_user
        self.balance = balance

