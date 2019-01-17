from functools import partial

from balebot.filters import *
from balebot.handlers import *
from balebot.models.messages import *
from balebot.utils.logger import Logger
from balebot.utils.util_functions import generate_random_id

from bot.api_handler import *
from bot.base_bot import Bot
from bot.callbacks import *
from bot.db_handler import *
# from bot.models.base import Base, engine
from constants import *

my_logger = Logger.get_logger()

main_bot = Bot()
bot = main_bot.bot
updater = main_bot.updater
dispatcher = main_bot.dispatcher
loop = main_bot.loop

# Base.metadata.create_all(engine)


########################

def _get_user(update):
    return update.get_effective_user()


def _get_message(update):
    return update.get_effective_message()


def _get_data(update, key):
    return dispatcher.get_conversation_data(update, key=key)


def _set_data(update, key, value):
    dispatcher.set_conversation_data(update, key, value)


######################## add admin ######################
@dispatcher.command_handler(Command.add_admin)
def ask_admin_id_add(bot, update):
    if update.users[0].id != BotConfig.root_admin:
        bot.respond(update, TextMessage(BotMessage.no_admin_right))
        dispatcher.finish_conversation(update)
        return
    bot.respond(update, TextMessage(BotMessage.add_admin_id))
    dispatcher.register_conversation_next_step_handler(update, general_handlers + [
        MessageHandler(TextFilter(pattern=Patterns.bale_id), adding_admin),
        MessageHandler(DefaultFilter(), ask_admin_id_add)
    ])


def adding_admin(bot, update):
    admin_id = update.get_effective_message().text
    user = add_admin(admin_id)
    bot.respond(update, TextMessage(
        BotMessage.add_admin.format(user.name, user.user_name)))
    dispatcher.finish_conversation(update)


@dispatcher.command_handler(Command.del_admin)
def choose_admin_id_del(bot, update):
    if update.users[0].id != BotConfig.root_admin:
        bot.respond(update, TextMessage(BotMessage.no_admin_right))
        dispatcher.finish_conversation(update)
        return

    admins = get_admins()
    general_message = TextMessage(BotMessage.choose_admin)
    bot.respond(update, TemplateMessage(general_message, [
        TemplateMessageButton(admin.User.name, admin.User.peer_id, ButtonAction.default) for admin in admins]))
    dispatcher.register_conversation_next_step_handler(update, general_handlers + [
        MessageHandler(TemplateResponseFilter(keywords=[admin.User.peer_id for admin in admins]), delete_admin),
        MessageHandler(DefaultFilter(), choose_admin_id_del)
    ])


def delete_admin(bot, update):
    admin_id = update.get_effective_message().text_message
    del_admin(admin_id)
    bot.respond(update, TextMessage(BotMessage.del_admin))
    dispatcher.finish_conversation(update)


######################## send_message ###################
def send_message(message, peer, step, user_input=None, succedent_message=None, attempt_number=SendingAttempt.first,
                 random_id=None):
    random_id = random_id if random_id else generate_random_id()
    kwargs = {UserData.user_peer: peer, UserData.step_name: step, UserData.succedent_message: succedent_message,
              UserData.message: message, UserData.attempt: attempt_number, UserData.send_message: send_message,
              UserData.user_input: user_input, UserData.loop: loop, UserData.random_id: random_id}
    bot.send_message(message=message, peer=peer, success_callback=step_success, failure_callback=step_failure,
                     kwargs=kwargs, random_id=random_id)


######################## conversation ###################

@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.return_to_main_menu))
@dispatcher.command_handler([Command.start])
@dispatcher.command_handler([Command.menu])
@dispatcher.default_handler()
def showing_menu(bot, update, state=State.default):
    add_user(update.users[0])
    user_input = update.get_effective_message()
    message = TemplateMessage(TextMessage(
        BotMessage.greeting if isinstance(user_input, TextMessage)
                               and user_input.text == Command.start else
        BotMessage.choose_from_menu if state == State.wrong else BotMessage.choose_from_menu),
        [
            TemplateMessageButton(ButtonMessage.start),
            TemplateMessageButton(ButtonMessage.guide),
        ])
    send_message(message, update.get_effective_user(), Step.showing_menu, user_input=user_input)
    dispatcher.finish_conversation(update)


@dispatcher.command_handler([Command.help])
@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonMessage.guide]))
def show_guide(bot, update):
    general_message = TextMessage(BotMessage.guide_text)
    btn_list = [
        TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu,
                              ButtonAction.default)
    ]
    message = TemplateMessage(general_message, btn_list)
    # p = BotConfig.location_guid_photo
    # photo_message = PhotoMessage(file_id=p['fileId'], access_hash=p['accessHash'], name=p['name'],
    #                              file_size=p['fileSize'], mime_type=p['mimeType'], thumb=p['thumb']['thumb'],
    #                              width=p['thumb']['width'], height=p['thumb']['height'], ext_width=p['ext']['width'],
    #                              ext_height=p['ext']['height'], caption_text=TextMessage("راهنمای ارسال موقعیت"),
    #                              file_storage_version=1)
    send_message(message, update.get_effective_user(), Step.show_guide, user_input=update.get_effective_message())
    dispatcher.finish_conversation(update)


################# show myid ##################
@dispatcher.command_handler(Command.myid)
def show_myid(bot, update):
    bot.respond(update, update.get_effective_user().peer_id)


#################### general handlers #################
general_handlers = [
    MessageHandler(TextFilter(exact=ButtonMessage.return_to_main_menu), showing_menu),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.return_to_main_menu), showing_menu),
    MessageHandler(TemplateResponseFilter(keywords=[ButtonMessage.guide]), show_guide),
    CommandHandler(Command.help, show_guide),
    CommandHandler(Command.start, showing_menu),
    CommandHandler(Command.add_admin, ask_admin_id_add),
    CommandHandler(Command.del_admin, choose_admin_id_del),
    CommandHandler(Command.myid, show_myid)
]


updater.run()
