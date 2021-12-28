import os
import base64
from Crypto.Cipher import AES
import json

from weixin.account.deadline import get_deadline, judge_deadline


def encode_state(openid, session_key):
    """
    加密算法：根据openid与access_key加密得到登录态
    补充空字符数 + openid + session_key + 补充空字符
    """
    data = get_deadline() + openid + session_key

    # 秘钥16位(通过环境变量取)
    aes_key = os.environ.get("BKAPP_AES_KEY")
    key = aes_key.encode()

    text = bytes(data.encode('utf-8'))

    for count in range(16 - (len(text) % 16) - 2):
        text += b'\0'
        # count += 1

    count += 1

    if count > 9:
        str_count = str(count)
    else:
        str_count = '0' + str(count)

    text = bytes(str_count.encode('utf-8')) + text

    aes = AES.new(key, AES.MODE_ECB)
    # 加密
    aes_code = aes.encrypt(text)

    # 编码
    encrypted_text = base64.encodebytes(aes_code)
    str_encrypted_text = bytes.decode(encrypted_text)
    j = json.dumps(str_encrypted_text)
    return j


def decode_state(state):
    """
    功  能: 解码登录态获得openid与session_key
    返回值:
           登录态未到期    message: True   data: (openid, session_key)
           登录态到期     message: False  data: None
    """
    aes_key = os.environ.get("BKAPP_AES_KEY")
    key = aes_key.encode()

    # 格式转换
    state = json.loads(state)
    str_encrypted_text = bytes(state, encoding='utf-8')
    bytes_encrypted_text = base64.decodebytes(str_encrypted_text)

    # 解码
    aes = AES.new(key, AES.MODE_ECB)
    aes_code = aes.decrypt(bytes_encrypted_text)

    # 如何将bytes类型转化为str
    str_aes_code = bytes.decode(aes_code)

    length = int(str_aes_code[0:2])
    deadline = str_aes_code[2:21]
    openid = str_aes_code[21:49]
    session_key = str_aes_code[49:len(str_aes_code)-length]

    if judge_deadline(deadline):
        return False, None

    return True, (openid, session_key)
