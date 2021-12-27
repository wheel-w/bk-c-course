import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Member, UserCourseContact


# Create your views here.
def is_teacher(fun):
    def inner(request, *args, **kwargs):
        try:
            user_id = request.user.id
            identity = Member.objects.filter(id=user_id).values(
                "identity"
            )  # 取出数据表中的identity值
            if (
                    identity.first()["identity"] == Member.Identity.TEACHER
            ):  # 将取出的Queryset转化为字典与字符串比较
                return fun(request, *args, **kwargs)
            else:
                return JsonResponse(
                    {"result": False, "code": 403, "message": "您没有操作权限！", "data": []}
                )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "code": 401, "message": "请求错误！用户id不存在", "data": []}
            )  # 返回信息

    return inner


@csrf_exempt
@is_teacher
def manage_course(request):
    # 增
    if request.method == "POST":
        user_id = request.user.id
        user = Member.objects.get(id=user_id)  # 获取当前登录用户
        course_name = request.POST.get("course_name", False)  # 想创建的课程名称
        teacher = request.POST.get("teacher", False)  # 授课教师
        if not (course_name and teacher):
            return JsonResponse(
                {
                    "result": False,
                    "message": "请检查您输入的课程姓名和您的教师工号姓名！",
                    "code": 400,
                    "date": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        course_introduction = request.POST.get("course_introduction", "无")  # 课程简介
        manage_student = request.POST.get("manage_student", "")  # 学生管理员
        news_course_info = Course.objects.create(
            course_name=course_name,
            course_introduction=course_introduction,
            teacher=teacher,
            create_people=user.username,
            manage_student=manage_student,
        )  # 将得到的数据加到course表
        UserCourseContact.objects.create(user_id=user_id, course_id=news_course_info.id)
        return JsonResponse(
            {"result": True, "message": "增加成功", "code": 201, "date": []},
            json_dumps_params={"ensure_ascii": False},
        )

    # 删
    if request.method == "DELETE":
        req = QueryDict(request.body)
        course_id = req.get("course_id")
        if not course_id:
            return JsonResponse(
                {"result": False, "message": "删除失败！课程id不能为空", "code": 400, "date": []},
                json_dumps_params={"ensure_ascii": False},
            )
        try:
            Course.objects.get(id=course_id)
            Course.objects.filter(id=course_id).delete()
            UserCourseContact.objects.filter(course_id=course_id).delete()
            return JsonResponse(
                {"result": True, "message": "删除成功", "code": 200, "date": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except Course.DoesNotExist:
            return JsonResponse(
                {
                    "result": False,
                    "message": "删除失败，您输入的课程id不存在！",
                    "code": 400,
                    "date": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )

    # 改
    if request.method == "PUT":
        req = QueryDict(request.body)
        course_id = req.get("course_id")
        if not course_id:
            return JsonResponse(
                {"result": False, "message": "修改失败！课程id不能为空", "code": 415, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        try:
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
        except Exception:
            return JsonResponse(
                {
                    "result": False,
                    "message": "修改失败，请检查您输入的格式是否正确或课程id是否存在",
                    "code": 415,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )


# 查
def search_courses_by_userid(request):
    if request.method == "GET":
        user_id = request.user.id
        course_ids = UserCourseContact.objects.filter(user_id=user_id).values_list(
            "course_id", flat=True
        )
        course = Course.objects.in_bulk(course_ids).values()
        courses = serializers.serialize(
            "json", course, ensure_ascii=False
        )
        return JsonResponse(
            {
                "result": True,
                "message": "查询成功",
                "code": 200,
                "data": courses,
            },
            json_dumps_params={"ensure_ascii": False},
        )
