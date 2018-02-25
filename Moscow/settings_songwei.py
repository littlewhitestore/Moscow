from settings import *

DATABASES = {
    'default': {
        'NAME': 'moscow',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {'init_command': 'SET default_storage_engine=InnoDB'},
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    }
}
