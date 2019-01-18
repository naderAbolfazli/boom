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
from bot.models.base import Base, engine
from bot.utils import validate_national_code
from constants import *

my_logger = Logger.get_logger()

main_bot = Bot()
bot = main_bot.bot
updater = main_bot.updater
dispatcher = main_bot.dispatcher
loop = main_bot.loop

Base.metadata.create_all(engine)


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
    add_admin(admin_id)
    bot.respond(update, TextMessage(
        BotMessage.add_admin))
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
    user = get_user(_get_user(update).peer_id)
    if user.national_id and user.authorization_code and user.access_token:
        user_input = update.get_effective_message()
        message = TemplateMessage(TextMessage(
            BotMessage.greeting if isinstance(user_input, TextMessage)
                                   and user_input.text == Command.start else
            BotMessage.choose_from_menu if state == State.wrong else BotMessage.choose_from_menu),
            [
                TemplateMessageButton(ButtonMessage.my_boom),
                TemplateMessageButton(ButtonMessage.my_services),
                TemplateMessageButton(ButtonMessage.hot_services),
                TemplateMessageButton(ButtonMessage.about_boom),
            ])
        send_message(message, _get_user(update), Step.showing_menu, user_input=user_input)
        dispatcher.finish_conversation(update)
    elif user.authorization_code:
        update_user_access_token(user.peer_id, user.authorization_code)
        showing_menu(bot, update)
    elif user.national_id:
        message = TemplateMessage(TextMessage(BotMessage.authorization_and_access), [
            TemplateMessageButton(ButtonMessage.access_granted)
        ])
        send_message(message, _get_user(update), Step.ask_national_id, _get_message(update))
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(DefaultFilter(), showing_menu)
        ])
    else:
        message = TemplateMessage(TextMessage(BotMessage.ask_national_id), [
            TemplateMessageButton(ButtonMessage.already_inserted)
        ])
        send_message(message, _get_user(update), Step.ask_national_id, _get_message(update))
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TextFilter(validator=validate_national_code), get_national_id),
            MessageHandler(DefaultFilter(), showing_menu)
        ])


def get_national_id(bot, update):
    national_id = _get_message(update).text
    update_user_national_id(_get_user(update).peer_id, national_id)
    showing_menu(bot, update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonMessage.about_boom]))
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


@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.my_boom))
def my_boom_menu(bot, update):
    message = TemplateMessage(TextMessage(BotMessage.choose_from_menu), [
        TemplateMessageButton(ButtonMessage.boom_information),
        TemplateMessageButton(ButtonMessage.booming),
        TemplateMessageButton(ButtonMessage.received_boom),
        TemplateMessageButton(ButtonMessage.sent_boom),
        TemplateMessageButton(ButtonMessage.return_to_main_menu)
    ])
    send_message(message, _get_user(update), Step.my_boom_menu, _get_message(update))
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.boom_information))
def boom_information(bot, update):
    message = TemplateMessage(TextMessage(generate_boom_information(_get_user(update).peer_id)), [
        TemplateMessageButton(ButtonMessage.return_to_main_menu)
    ])
    send_message(message, _get_user(update), Step.boom_information, _get_message(update))
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.booming))
def booming(bot, update):
    pass
    # message =


@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.received_boom))
@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.sent_boom))
def show_my_booms(bot, update):
    user_ipnut = _get_message(update).text
    if user_ipnut == ButtonMessage.sent_boom:
        credits = get_sent_credits(_get_user(update).peer_id)
        msg = BotMessage.sent_credit
    else:
        credits = get_received_credits(_get_user(update).peer_id)
        msg = BotMessage.received_credit
    for credit in credits:
        message = TextMessage(
            msg.format(credit.to_user if user_ipnut == ButtonMessage.sent_boom else credit.from_user, credit.balance,
                       credit.date_time))
        send_message(message, _get_user(update), Step.show_my_booms)
    loop.call_later(1, send_message, TemplateMessage(TextMessage(
        "انتقالات بوم را در بالا مشاهده میکنید." if credits.__len__() else "انتقالات بوم برای شما *یافت نشد.*"), [
        TemplateMessageButton(ButtonMessage.return_to_main_menu)
    ]),
                    _get_user(update), _get_message(update))
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.my_services))
def show_my_services(bot, update):
    financial_services = get_user_financial_services(_get_user(update).peer_id)
    for service in financial_services:
        message = TextMessage(BotMessage.financial_service.format(service.category, service.title, service.description,
                                                                  service.phone_number, service.date_time))
        send_message(message, _get_user(update), Step.show_my_services)
    loop.call_later(1, send_message, TemplateMessage(TextMessage(
        "تسهیلات خود را در بالا مشاهده میکند." if financial_services.__len__() else "تسهیلات فعالی برای شما *یافت نشد.*"),
        [
            TemplateMessageButton(
                ButtonMessage.register_my_service_manually),
            TemplateMessageButton(ButtonMessage.return_to_main_menu)
        ]),
                    _get_user(update), _get_message(update))
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(exact=ButtonMessage.hot_services))
def choose_hot_services_category(bot, update):
    message = TemplateMessage(TextMessage(BotMessage.choose_from_menu), [
        TemplateMessageButton(ButtonMessage.housing),
        TemplateMessageButton(ButtonMessage.home_appliances),
        TemplateMessageButton(ButtonMessage.investment_fund),
    ])
    send_message(message, _get_user(update), Step.show_hot_services, _get_message(update))
    dispatcher.register_conversation_next_step_handler(update, general_handlers + [
        MessageHandler(TemplateResponseFilter(
            keywords=[ButtonMessage.housing, ButtonMessage.home_appliances, ButtonMessage.investment_fund]),
            show_hot_services),
        MessageHandler(DefaultFilter(), choose_hot_services_category)
    ])


def show_hot_services(bot, update):
    category = _get_message(update).text
    hot_services = get_services_by_category(_get_user(update).peer_id, category)
    for service in hot_services:
        message = TextMessage(
            BotMessage.financial_service.format(service.category, service.title, service.description,
                                                service.phone_number, service.date_time))
        send_message(message, _get_user(update), Step.show_my_booms)
    loop.call_later(1, send_message, TemplateMessage(TextMessage(
        "تسهیلات را در بالا مشاهده میکنید." if hot_services.__len__() else "تسهیلاتی متناسب با جستجو *یافت نشد.*"), [
        TemplateMessageButton(ButtonMessage.return_to_main_menu)
    ]), _get_user(update), Step.show_hot_services, _get_message(update))


################# show myid ##################
@dispatcher.command_handler(Command.myid)
def show_myid(bot, update):
    bot.respond(update, update.get_effective_user().peer_id)


#################### general handlers #################
general_handlers = [
    MessageHandler(TextFilter(exact=ButtonMessage.return_to_main_menu), showing_menu),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.return_to_main_menu), showing_menu),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.about_boom), show_guide),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.my_boom), my_boom_menu),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.booming), booming),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.boom_information), boom_information),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.hot_services), choose_hot_services_category),
    MessageHandler(TemplateResponseFilter(exact=ButtonMessage.my_services), show_my_services),
    CommandHandler(Command.start, showing_menu),
    CommandHandler(Command.add_admin, ask_admin_id_add),
    CommandHandler(Command.del_admin, choose_admin_id_del),
    CommandHandler(Command.myid, show_myid)
]

updater.run()
