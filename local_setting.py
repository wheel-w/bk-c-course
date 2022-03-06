from config import APP_CODE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "xaut-saas",
        "USER": "root", #数据库用户名
        "PASSWORD": "zsy21sjz", #数据库密码
        "HOST": "localhost",
        "PORT": "3306",
    },
}