import os


# 获取项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))


'''
以下秘钥为前后端加密网络请求使用，更改需同时更改前后端代码中的秘钥，否则会无法获取数据
'''

# # 用户模块session秘钥
SECRET_KEY = 'bwhy'


# 验证相关

# 时间戳验证位数，0-9中的任意个数数字
TIMESTAMP_SUB = [3, 7]
# 最大时间差，单位：秒
TIME_DIFFERENCE = 150
# 签名加密密钥，需与前端同步修改
SIGN_KEY = 'jumei'

# URL加密密钥，需与前端同步修改
URL_KEY = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# mongoDB配置,默认地址为localhost,端口27017
# URI为地址，DB为数据库名, PWD为密码
MONGO_URI = 'localhost'
MONGO_DB = 'shopping'
MONGO_PWD = 'heiwokusiquanjia!'

# redis密码
REDIS_PWD = 'heiwokusiquanjia!'

# sqlite3配置,默认地址localhost,端口6379
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/config', 'Shopping.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True


# api地址和端口
# 修改端口的同时需修改服务器端口映射，HOST会自动替换为本机IP
HOST = '0.0.0.0'
PORT = '5003'


# 短信API相关
MESSAGE_USER = 'E10CA4'
MESSAGE_PASSWORD = '9S4545'
MESSAGE_URL = 'http://api02.monyun.cn:7901/sms/v2/std/'

# 物流API相关
EXPRESS_KEY = 'd00fb20801418e04'
EXPRESS_URL = 'https://api.jisuapi.com/express/query'

# 用户上传头像地址
HEAD_PATH = basedir + '/static/headers/'
# IMG_PATH = 'http://192.168.1.103:5003/v5/show/'
IMG_PATH = 'http://47.97.204.150:5003/v5/show/'

# 评论上传图片地址
COMMENT_PATH = basedir + '\\static\\comments\\'
# COMMENT_IMG_PATH = 'http://192.168.1.103:5003/v5/show_comment/'
COMMENT_IMG_PATH = 'http://47.97.204.150:5003/v5/show_comment/'

# 静态文件前缀
STATIC_URL_PATH = '/static'
# 静态文件目录
STATIC_FOLDER = 'static'
# 模板目录
TEMPLATE_FOLDER = '/templates'
