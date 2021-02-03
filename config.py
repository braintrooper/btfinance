import os

class Config(object):
    DEBUG = True
    API_KEY="pk_0b7836d41c7242dea1bb7cd597271bc0"
    SECRET_KEY="88d1981e66212cc31e5f12d20f4bdb09aff75edf6c7cf88a"
    DEBUG_VALUE="True"
    EMAIL_USER=os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD=os.environ.get('EMAIL_PASS')

