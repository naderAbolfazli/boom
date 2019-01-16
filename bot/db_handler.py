from balebot.utils.logger import Logger
from bot.models.admin import Admin
from bot.models.base import Session
from bot.models.user import User
from constants import LogMessage, UserData

session = Session()
my_logger = Logger.get_logger()


def add_admin(user_id):
    user = get_user(user_id)
    if user:
        admin = Admin(user)
        session.add(admin)
        session.commit()
    return user


def del_admin(peer_id):
    admin = session.query(Admin).filter(Admin.peer_id == peer_id).one_or_none()
    session.delete(admin)
    session.commit()


def get_admins():
    admins = session.query(Admin, User).filter(Admin.peer_id == User.id).all()
    return [admin.peer_id for admin in admins]


def get_admin(peer_id) -> Admin:
    return session.query(Admin).filter(Admin.peer_id == peer_id).one_or_none()


def add_user(user):
    if get_user(user.id):
        return
    user = User(user.id, user.access_hash, name=user.name, user_name=user.username, sex=user.sex)
    session.add(user)
    session.commit()
    my_logger.info(LogMessage.user_register,
                   extra={UserData.user_id: user.id, "tag": "info"})


def get_user(peer_id) -> User:
    user = session.query(User).filter(User.peer_id == peer_id).one_or_none()
    return user


