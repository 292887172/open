# 是否开启调试
IS_DEBUG = True

# 静态资源路径
STATIC_URL_CONF = '/static/'
# STATIC_URL = 'android-assets/static/'

# session 超时时间（单位秒）
SESSION_TIMEOUT = 60 * 120

# 服务器域名,发验证邮件
HOST_DOMAIN = 'http://localhost:8000'

# 云存储token值
#CLOUD_TOKEN = "5630838a6f43f66846246d8b"  # 支持所有
CLOUD_TOKEN = "5630841e6f43f668994af13c"  # open

# 消息验证服务器接口地址
VALIDATE_URL = "http://localhost:8080/messages/verify_message"

# 产品key值验证服务器接口
KEY_URL = "https://oven.53iq.com/api/produce/base_html"
