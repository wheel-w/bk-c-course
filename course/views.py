from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Member, UserCourseContact

# Create your views here.


def is_teacher(fun):
    def inner(request, *args, **kwargs):
        try:
            user_name = request.user.username
            identity = Member.objects.filter(username=user_name).values(
                "identity"
            )  # 取出数据表中的identity值
            if (
                identity.first()["identity"] == Member.Identity.TEACHER
            ):  # 将取出的Queryset转化为字典与字符串比较
                return fun(request, *args, **kwargs)
            else:
                return JsonResponse(
                    {"result": False, "code": 403, "message": "您没有操作权限", "data": []}
                )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "code": 401, "message": "请求错误！", "data": []}
            )  # 返回信息

    return inner


@csrf_exempt
@is_teacher
def manage_course(request):
    # 增
    if request.method == "POST":
        try:
            user_id = request.user.id
            try:
                user_name = Member.objects.get(id=user_id)  # 获取当前登录用户的名称
            except ObjectDoesNotExist as e:
                return JsonResponse(
                    {
                        "result": False,
                        "message": "增加失败，异常信息：{}".format(e),
                        "code": 400,
                        "date": [],
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
            course_name = request.POST.get("course_name", "未添加")  # 想创建的课程名称
            course_introduction = request.POST.get("course_introduction", "无")  # 课程简介
            teacher = request.POST.get("teacher", user_name.username)  # 授课教师
            manage_student = request.POST.get("manage_student", "")  # 学生管理员
            news_course_info = Course.objects.create(
                course_name=course_name,
                course_introduction=course_introduction,
                teacher=teacher,
                create_people=user_name.username,
                manage_student=manage_student,
            )  # 将得到的数据加到course表
            UserCourseContact.objects.create(
                user_id=user_id, course_id=news_course_info.id
            )
            return JsonResponse(
                {"result": True, "message": "增加成功", "code": 201, "date": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except Exception as e:
            return JsonResponse(
                {
                    "result": False,
                    "message": "增加失败，异常信息：{}".format(e),
                    "code": 400,
                    "date": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        # 删
    if request.method == "DELETE":
        req = QueryDict(request.body)
        course_id = req.get("course_id")
        if not bool(req.get("course_id")):
            return JsonResponse(
                {"result": False, "message": "删除失败！课程id不能为空", "code": 400, "date": []},
                json_dumps_params={"ensure_ascii": False},
            )
        try:
            Course.objects.get(id=course_id).delete()
            UserCourseContact.objects.get(course_id=course_id).delete()
            return JsonResponse(
                {"result": True, "message": "删除成功", "code": 200, "date": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except ObjectDoesNotExist as e:
            return JsonResponse(
                {
                    "result": False,
                    "message": "删除失败，请核对您输入的信息!异常信息：{}".format(e),
                    "code": 400,
                    "date": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )

    # 改
    if request.method == "PUT":
        req = QueryDict(request.body)
        try:
            if not bool(req.get("course_id")):
                return JsonResponse(
                    {"result": False, "message": "课程id不能为空", "code": 415, "data": []},
                    json_dumps_params={"ensure_ascii": False},
                )
            else:
                course_id = req.get("course_id")
                course = Course.objects.get(id=course_id)
                course.course_name = req.get("course_name", course.course_name)
                course.course_introduction = req.get(
                    "course_introduction", course.course_introduction
                )
                course.teacher = req.get("teacher", course.teacher)
                course.manage_student = req.get("manage_student", Course.manage_student)
                course.save()
                return JsonResponse(
                    {"result": True, "message": "修改成功", "code": 200, "data": []},
                    json_dumps_params={"ensure_ascii": False},
                )
        except Exception as e:
            return JsonResponse(
                {
                    "result": False,
                    "message": "修改出现异常，异常信息为:{}".format(e),
                    "code": 415,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )


# 查
def search_courses_by_userid(request):
    if request.method == "GET":
        try:
            user_id = request.user.id
            course_ids = UserCourseContact.objects.filter(user_id=user_id).values_list(
                "course_id", flat=True
            )
            if bool(course_ids):
                course_names = Course.objects.in_bulk(course_ids).values()
                course_name = serializers.serialize(
                    "json", course_names, ensure_ascii=False
                )
                return JsonResponse(
                    {
                        "result": True,
                        "message": "查询成功",
                        "code": 200,
                        "id": user_id,
                        "data": course_name,
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
            else:
                return JsonResponse(
                    {
                        "result": False,
                        "message": "所查询用户没有相关课程",
                        "code": 404,
                        "id": user_id,
                        "data": [],
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
        except Exception as e:
            return JsonResponse(
                {
                    "result": False,
                    "message": "查询出现异常，异常信息为:{}".format(e),
                    "code": 404,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
