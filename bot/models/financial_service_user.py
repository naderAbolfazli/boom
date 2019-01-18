import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from bot.models.base import Base


class FinancialServiceUser(Base):
    __tablename__ = "financial_service_usre"
    id = Column(Integer, primary_key=True)
    financial_service_id = Column(Integer, ForeignKey("financial_services.id"))
    financial_service = relationship("FinancialService",
                                     backref=backref("financial_service_usre", cascade="all, delete-orphan"))
    client_national_id = Column(String(10))
    date_time = Column(DateTime)

    def __init__(self, financial_service, client_national_id):
        self.financial_service = financial_service
        self.client_national_id = client_national_id
        self.date_time = datetime.datetime.now()
