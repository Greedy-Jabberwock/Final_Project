import os


class Config:

    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    db_info = {
        'user': os.environ.get("PG_USER"),
        'psw': os.environ.get("PG_PSW"),
        'host': 'localhost',
        'database': 'final_project',
        'port': ''
    }
    SQLALCHEMY_DATABASE_URI = f'postgresql://' \
                              f'{db_info["user"]}:' \
                              f'{db_info["psw"]}@' \
                              f'{db_info["host"]}/' \
                              f'{db_info["database"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.mail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USER")
    MAIL_PASSWORD = os.environ.get("MAIL_PSW")

