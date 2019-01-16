from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from bot.models.base import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, pripmary_key=True)
    peer_id = Column(String, unique=True)
    type = Column(String)

    def __init__(self, peer_id, type=None):
        self.peer_id = peer_id
        self.type = type
