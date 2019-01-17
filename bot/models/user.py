from sqlalchemy import Column, Integer, String, ForeignKey

from bot.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String)
    user_name = Column(String)
    national_code = Column(String)

    def __init__(self, peer_id,user_name,national_code):
        self.peer_id = peer_id
        self.user_name = user_name
        self.national_code = national_code
