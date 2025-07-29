import os


# URL
HW_OA_API_URL = os.getenv("hwoa_url","http://v-test85-centos7")
# token
APP_NAME = os.getenv("app_name","qywx_api")
APP_SECRET = os.getenv("app_secret","U2FsdGVkX19aeklYjFEVoSjz4N1296H7Nzs9AoUX")

USER_AGENT = "hwoa-mcp-server/1.0"


from .account import *