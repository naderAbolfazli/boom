import os


class BotConfig:
    root_admin = os.getenv('BOT_ADMIN_ID', '1471278867')
    reports_route = "files/"
    base_url = os.getenv('BASE_URL', "wss://api.bale.ai/v1/bots/")
    bot_token = os.getenv('TOKEN', "0f8c34cd08e81d3604f23f712a095f167dfc37d8")
    system_local = os.getenv('SYSTEM_LOCAL', "fa_IR")
    resending_max_try = int(os.getenv('RESENDING_MAX_TRY', 5))
    reuploading_max_try = int(os.getenv('REUPLOADING_MAX_TRY', 5))


class DbConfig:
    db_user = os.getenv('DB_USER', "admin")
    db_password = os.getenv('DB_PASSWORD', "nader1993")
    db_host = os.getenv('DB_HOST', "localhost")
    db_name = os.getenv('DB_NAME', "boom")
    db_port = os.getenv('DB_PORT', "3306")
    database_url = "mysql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name) or None
