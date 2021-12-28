import datetime

# 登录态的有效时间
VALID_TIME = 6


def get_deadline():
    """
    获取登录态的失效时间 (当前时间 + 登录态的有效时间)
    """

    deadline = datetime.datetime.now() + datetime.timedelta(hours=VALID_TIME)

    str_deadline = str(deadline).split('.')[0]
    return str_deadline


def judge_deadline(str_deadline):
    """
    判断登录态是否到期
    """
    now = datetime.datetime.now()
    deadline = datetime.datetime.strptime(str_deadline, "%Y-%m-%d %H:%M:%S")

    if now > deadline:
        return True
    else:
        return False
