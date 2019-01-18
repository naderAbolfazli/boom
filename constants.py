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


oauth_url = "http://pfm.myoxygen.ir/auth/realms/master/protocol/openid-connect/auth?response_type=code&state=&client_id=f741487d-872f-46f8-82ae-b447165d&client_secret=f8e30e8c-cb4c-407e-89cd-fa885a2c9f7c&scope=&redirect_uri=http://172.31.111.54"


class BotMessage:
    ask_credit_balance = "مبلغ اعتبار"
    ask_receiver_national_id = "کد ملی گیرنده:"
    financial_service = "دسته بندی: {}\nعنوان: *{}*\nتوضیحات: {}\nشماره تلفن: *{}*\nتاریخ: {}"
    sent_credit = "کد ملی گیرنده: *{}*\nمبلغ: *{}*\nتاریخ: {}"
    received_credit = "کد ملی فرستنده: *{}*\nمبلغ: *{}*\nتاریخ: {}"
    authorization_and_access = "احراز هویت و تخصیص دسترسی ها را از طریق لینک زیر انجام دهید:\n" \
                               "[احراز هویت]({})".format(oauth_url)
    ask_national_id = "لطفا ابتدا *کد ملی* خود را وارد نمایید:"
    add_admin_id = "لطفا آی دی ادمین جدید را وارد کنید:"
    no_admin_right = "*شما دسترسی ادمین روت ندارید!*"
    del_admin = "ادمین مورد نظر حذف شد"
    add_admin = "ادمین جدید با موفقیت اضافه شد."
    choose_admin = "ادمین مورد نظر را انتخاب کنید:"
    guide_text = "کاربر گرامی به *Boom* خوش آمدید.\n" \
                 "به کمک این بازو میتوانید از خدمات *بانکداری و مدیریت مالی* (بوم) استفاده نمائید.\n" \
                 "پیشاپیش از حسن اعتماد شما سپاسگذاریم"
    enter_your_pass = "رمز عبور خود را وارد کنید"
    choose_from_menu = "یکی از موارد زیر را انتخاب کنید"
    greeting = "سلام به بازوی *بوم* خوش آمدید"


class ButtonMessage:
    back = "بازگشت"
    register_booming = "🔴ثبت بومینگ🔴"
    credit_balance = "مبلغ اعتبار"
    receiver_national_id = "کد ملی گیرنده"
    investment_fund = "صندوق سرمایه گذاری"
    home_appliances = "لوازم خانگی"
    housing = "مسکن"
    register_my_service_manually = "ثبت دستی تسهیلات جدید"
    sent_boom = "بوم های ارسالی"
    received_boom = "بوم های دریافتی"
    booming = "بومینگ"
    boom_information = "اطلاعات بوم"
    access_granted = "احراز هویت و تخصیص دسترسی انجام شد"
    already_inserted = "قبلا وارد کرده ام"
    about_boom = "درباره بوم"
    hot_services = "پیشنهادات داغ"
    my_services = "تسهیلات من"
    my_boom = "بوم من"
    start = "شروع"
    report = "گزارش"
    yes = "بله"
    return_to_main_menu = "بازگشت به منو"
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
    register_booming = "register_booming"
    ask_boomin_info = "ask_booming_info"
    booming = "booming"
    show_hot_services = "show_hot_services"
    show_my_services = "show_my_services"
    show_my_booms = "show_my_booms"
    boom_information = "boom_information"
    my_boom_menu = "my_boom_menu"
    ask_national_id = "ask_national_id"
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
    credit_balance = "credit_balance"
    receiver_national_id = "receiver_national_id"
    peer_id = "peer_id"
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
