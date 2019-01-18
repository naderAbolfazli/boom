from typing import Sequence

from unidecode import unidecode

from balebot.utils.logger import Logger
from bot.api_handler import get_access_token
from bot.models.admin import Admin
from bot.models.base import Session
from bot.models.credit import Credit
from bot.models.financial_service import FinancialService
from bot.models.financial_service_user import FinancialServiceUser
from bot.models.user import User
from constants import LogMessage, UserData

session = Session()
my_logger = Logger.get_logger()


def add_admin(user_id):
    admin = Admin(user_id)
    session.add(admin)
    session.commit()


def del_admin(peer_id):
    admin = session.query(Admin).filter(Admin.peer_id == peer_id).one_or_none()
    session.delete(admin)
    session.commit()


def get_admins():
    admins = session.query(Admin).all()
    return [admin.peer_id for admin in admins]


def get_admin(peer_id) -> Admin:
    return session.query(Admin).filter(Admin.peer_id == peer_id).one_or_none()


def add_user(user):
    if get_user(user.id):
        return
    user = User(user.id, user_name=user.username)
    session.add(user)
    session.commit()
    my_logger.info(LogMessage.user_register,
                   extra={UserData.user_id: user.id, UserData.peer_id: user.peer_id, "tag": "info"})


def update_user_national_id(peer_id, national_id):
    user = get_user(peer_id)
    user.national_id = unidecode(national_id)
    session.commit()


def update_user_access_token(peer_id, authorization_code):
    user = get_user(peer_id)
    result = get_access_token(authorization_code)
    user.access_token = result.get('access_token')
    session.commit()


def get_user(peer_id) -> User:
    user = session.query(User).filter(User.peer_id == peer_id).one_or_none()
    return user


def generate_boom_information(peer_id):
    user = get_user(peer_id)
    return "boom info"


def get_sent_credits(peer_id):
    user = get_user(peer_id)
    credits = session.query(Credit).filter(Credit.from_user == user.national_id).all()
    return credits


def get_received_credits(peer_id):
    user = get_user(peer_id)
    credits = session.query(Credit).filter(Credit.to_user == user.national_id).all()
    return credits


def get_user_financial_services(peer_id) -> Sequence[FinancialService]:
    user = get_user(peer_id)
    results = session.query(FinancialServiceUser).filter(
        FinancialServiceUser.client_national_id == user.national_id).all()
    return [result.financial_service for result in results]
