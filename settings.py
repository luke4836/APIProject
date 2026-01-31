import os  
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': os.environ.get('MYSQL_DATABASE', 'zeabur'),  
        'USER': os.environ.get('MYSQL_USER', 'root'),  
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),  
        'HOST': os.environ.get('MYSQL_HOST', 'localhost'),  
        'PORT': os.environ.get('MYSQL_PORT', '3306'),  
        'OPTIONS': {  
            'charset': 'utf8mb4',  
        }  
    }  
}  
ALLOWED_HOSTS = ['*']  
INSTALLED_APPS = [  
    'django.contrib.admin',  
    'django.contrib.auth',  
    'django.contrib.contenttypes',  
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'django.contrib.staticfiles',  
    'Api',  # 添加這一行  
]  
