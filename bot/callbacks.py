import functools
import os

from balebot.models.constants.file_type import FileType
from balebot.models.messages import TextMessage, DocumentMessage
from balebot.utils.logger import Logger
from config import BotConfig
from constants import UserData, LogMessage, MimeType, BotMessage, SendingAttempt, Step

my_logger = Logger.get_logger()


def step_success(response, user_data):
    user_data = user_data.get(UserData.kwargs)
    user_peer = user_data.get(UserData.user_peer)
    step_name = user_data.get(UserData.step_name)
    user_input = user_data.get(UserData.user_input)
    my_logger.info(LogMessage.successful_step_message_sending,
                   extra={UserData.user_id: user_peer.peer_id, UserData.bot_message: user_data.get(UserData.message),
                          UserData.step_name: step_name, UserData.user_input: user_input, "tag": "info"})
    if user_data.get(UserData.succedent_message):
        send_message = user_data.get(UserData.send_message)
        loop = user_data.get(UserData.loop)
        step_name = user_data.get(UserData.step_name)
        succedent_message = user_data.get(UserData.succedent_message)
        loop.call_soon(send_message, succedent_message, user_peer, step_name)


def step_failure(response, user_data):
    user_data = user_data.get(UserData.kwargs)
    user_peer = user_data.get(UserData.user_peer)
    step_name = user_data.get(UserData.step_name)
    user_input = user_data.get(UserData.user_input)
    send_message = user_data.get(UserData.send_message)
    loop = user_data.get(UserData.loop)
    random_id = user_data.get(UserData.random_id)
    message = user_data.get(UserData.message)
    user_data[UserData.attempt] += 1
    my_logger.error(LogMessage.failed_step_message_sending,
                    extra={UserData.user_id: user_peer.peer_id, UserData.bot_message: message,
                           UserData.step_name: step_name, UserData.user_input: user_input, "tag": "error"})
    if user_data.get(UserData.attempt) <= BotConfig.resending_max_try:
        loop.call_soon(
            functools.partial(send_message, message, user_peer, step_name, attempt_number=user_data[UserData.attempt],
                              random_id=random_id))
        return
    my_logger.error(LogMessage.failed_step_message_sending_after_max_try.format(BotConfig.resending_max_try),
                    extra={UserData.user_id: user_peer.peer_id, UserData.bot_message: user_data.get(UserData.message),
                           UserData.step_name: step_name, UserData.user_input: user_input, "tag": "error"})
