from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blueapps.account.decorators import login_exempt
from course.models import Member
from .api.get_openid import verify_weixin_code
from .api.verify_account import identify_user
from .account.login_state import encode_state, decode_state


@login_exempt
def is_bind_wxuser(request):
    """
    功能：检查该微信用户是否绑定
    输入：request头中带有code
    返回：成功: result: True; data: state + user_id
         失败: result: False; data: state
    失败要求用户认证
    """
    code = request.GET.get('code')

    try:
        # 通过code换取openid与session_key
        session_key, openid = verify_weixin_code(code)
        # 获取登录态
        state = encode_state(session_key=session_key, openid=openid)
    except Exception as e:
        data = {
            'result': False,
            'message': e,
            'code': 500,
        }
        return JsonResponse(data)

    user = Member.objects.filter(openid=openid)
    if user.exists():
        user_id = user.values()[0].get('id')
        data = {
            'result': True,
            'message': '已认证',
            'code': 200,
            'data': {
                'state': state,
                'user_id': user_id,
            }
        }

        return JsonResponse(data)
    else:
        data = {
            'result': False,
            'message': '未认证',
            'code': 401,
            'data': {
                'state': state
            }
        }
        return JsonResponse(data)


@login_exempt
@csrf_exempt
def verify_schooluser(request):
    """
    功能：通过学分制的账号密码, 进行验证, 并绑定用户
    输入：request头中带有username,password,state
    返回：登录态过期：result: False; data: state
         认证成功： result: True; data: state, user_id
         认证失败： result: False; data: state
    """
    if request.method == 'POST':
        username = request.POST.get("name")
        password = request.POST.get("password")
        state = request.META.get("HTTP_COOKIE")

        try:
            # 解码登录态，并判断登录态是否到期
            result, data = decode_state(state)
            if not result:
                data = {
                    'result': False,
                    'message': '登录过期',
                    'code': 401,  # 用户未认证
                    'data': {
                        'state': state
                    }
                }
                return JsonResponse(data)

            openid, session_key = data[0], data[1]

            # 验证学分制账号与密码
            code, user_info = identify_user(username=username, password=password)
        except Exception as e:
            data = {
                'result': False,
                'message': e,
                'code': 500,  # 后端出错
                'data': {
                    'state': state,
                }
            }
            return JsonResponse(data)

        if code is 1:
            user = Member.objects.filter(openid=openid)
            if user.exists():
                user_id = user.values()[0].get('id')
                user.update(
                    class_number=user_info['user_name'],
                    name=user_info['user_real_name'],
                    professional_class=user_info['user_class'],
                    gender=user_info['user_sex'] == '男' and Member.Gender.MAN or Member.Gender.WOMAN,
                    identity=Member.Identity.STUDENT,
                    college=user_info['user_college']
                )
            else:
                user = Member.objects.create(
                    username=username + 'X',
                    openid=openid,
                    class_number=user_info['user_name'],
                    name=user_info['user_real_name'],
                    professional_class=user_info['user_class'],
                    gender=user_info['user_sex'] == '男' and Member.Gender.MAN or Member.Gender.WOMAN,
                    identity=Member.Identity.STUDENT,
                    college=user_info['user_college']
                )
                user_id = user.id
            data = {
                'result': True,
                'message': '认证成功',
                'code': 201,
                'data': {
                    'state': state,
                    'user_id': user_id,
                }
            }

            return JsonResponse(data)
        else:
            if code is 2:
                data = {
                    'result': False,
                    'message': '密码错误',
                    'data': {
                        'state': state,
                    }
                }
                return JsonResponse(data)
            else:
                if code is 3:
                    data = {
                        'result': False,
                        'message': '用户名不存在',
                        'data': {
                            'state': state,
                        }
                    }
                    return JsonResponse(data)
