import os
import requests


def request_wxapi(**query_param):
    """
    使用POST方法请求微信接口
    """
    weixin_check_code_url = 'https://api.weixin.qq.com/sns/jscode2session'
    resp = requests.get(url=weixin_check_code_url, params=query_param)
    resp.encoding = "utf-8"
    resp = resp.json()
    return resp


def verify_weixin_code(code):
    """
    code: 通过小程序发来的code, 获取openid
    验证code，并获取openid与access_token
    """

    # 构造参数
    query_param = {
        'appid': os.environ.get('BKAPP_APPID'),
        'secret': os.environ.get('BKAPP_SECRET'),
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    user_info = request_wxapi(**query_param)

    openid = user_info.get("openid")
    session_key = user_info.get("session_key")

    return session_key, openid
