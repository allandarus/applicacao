import os
import random
import string


class Config(object):
    CSRF_ENABLED = True
    SECRET = 'ysb_92=qe#djf8%ng+a*#4rt#5%3*4k5%i2bck*gn@w3@f&-&'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:hmetal85@localhost:3306/livro_flask'
    SENGRID_API_KEY = 'API_KEY'


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 8000
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'  # Trocar para ip quando subir o servidor de teste
    PORT_HOST = 5000
    URL_MAIN = f'http:{IP_HOST}:{PORT_HOST}/'  # Testar nova forma pythonica


class ProducingConfig(Config):
    TESTING = False
    DEBUG = False
    IP_HOST = 'localhost'  # Trocar para ip quando subir o servidor de produção
    PORT_HOST = 8080
    URL_MAIN = f'http://{IP_HOST}:{PORT_HOST}/'


app_config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'producing': ProducingConfig()
}

app_active = os.getenv('FLASK_ENV')
