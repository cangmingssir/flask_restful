# coding:utf-8
import os


#设置上传文件存放的位置
#os.path.abspath(__name__)  表示当前文件的当前路径
#os.path.dirname()  上一级目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
STATIC_DIR=os.path.join(BASE_DIR,'static')
MEDIA_DIR = os.path.join(STATIC_DIR,'uploads')


class Config():
    DEBUG = True
    ENV = 'development'

    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@localhost:3306/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #设置session相关参数
    SECRET_KEY = '7373737skfkejfekjf2838383'

