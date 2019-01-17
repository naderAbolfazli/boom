class Command:
    del_admin = "/del_admin"
    add_admin = "/add_admin"
    myid = "/myid"
    help = "/help"
    start = "/start"
    menu = "/menu"


class ButtonAction:
    default = 0


class Patterns:
    bale_id = "^\d{3,}$"
    phone_number_pattern = "^(\+98|0)?9\d{9}$"  # "(^09[0-9]{9}$)|(^9[0-9]{9}$)"
    fullname = "[\D]{7,130}"  # "^[\sآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی‬ٌ ‬ًّ ‬َ ‬ِ ‬ُ ‬]{5,30}$"  # "[\u0600-\u06FF\s]{5,30}"


class MimeType:
    image = "image/jpeg"
    csv = "text/csv"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class BotMessage:
    add_admin_id = "لطفا آی دی ادمین جدید را وارد کنید:"
    no_admin_right = "*شما دسترسی ادمین روت ندارید!*"
    del_admin = "ادمین مورد نظر حذف شد"
    add_admin = "ادمین جدید با موفقیت اضافه شد."
    choose_admin = "ادمین مورد نظر را انتخاب کنید:"
    guide_text = "این راهنما است."
    enter_your_pass = "رمز عبور خود را وارد کنید"
    choose_from_menu = "یکی از موارد زیر را انتخاب کنید"
    greeting = "سلام به بازوی *بوم* خوش آمدید"


class ButtonMessage:
    start = "شروع"
    report = "گزارش"
    yes = "بله"
    return_to_main_menu = "بازگشت به منوی اصلی"
    guide = "راهنما"


class State:
    edit = 4
    get_input = 3
    get_media = 2
    default = 1
    wrong = -1


class SendingAttempt:
    first = 1


class Step:
    show_guide = "show_guide"
    showing_menu = "showing_menu"
    conversation_starter = "conversation_starter"


class LogMessage:
    failed_step_message_sending_after_max_try = "failed step message sednig after {} try"
    user_register = "successful user register"
    successful_sending = "successful sending of message:"
    failed_sending = "failed sending of message:"
    successful_step_message_sending = "successful step message sending"
    failed_step_message_sending = "failure step message sending"


class UserData:
    send_message = "send_message"

    bot_message = "bot_message"
    loop = "loop"
    user_input = "user_input"
    url = "url"
    file_id = "file_id"
    succedent_message = "succedent_message"
    bot = "bot"
    logger = "logger"
    session = "session"
    random_id = "random_id"
    sending_attempt = "sending_attempt"
    kwargs = "kwargs"
    user_id = "user_id"
    user_peer = "user_peer"
    step_name = "step_name"
    message = "message"
    attempt = "attempt"
    report_attempt = "report_attempt"
