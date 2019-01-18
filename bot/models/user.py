from sqlalchemy import Column, Integer, String, ForeignKey, Text

from bot.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String(15))
    user_name = Column(String(40))
    national_id = Column(String(10))
    authorization_code = Column(Text)
    access_token = Column(Text)
    refresh_token = Column(Text)

    def __init__(self, peer_id, user_name):
        self.peer_id = peer_id
        self.user_name = user_name
