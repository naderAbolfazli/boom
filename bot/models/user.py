from sqlalchemy import Column, Integer, String

from bot.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String)
    access_hash = Column(String)
    name = Column(String)
    user_name = Column(String)
    sex = Column(String)

    def __init__(self, peer_id, access_hash, name, user_name, sex):
        self.peer_id = peer_id
        self.access_hash = access_hash
        self.name = name
        self.user_name = user_name
        self.sex = sex
