import json
import logging

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.http import JsonResponse

from blueapps.core.exceptions import DatabaseError
from weixin.api.verify_account import identify_user

from .models import Course, Member, UserCourseContact

# Create your views here.


def update_user_info(request):
    """
    更新用户信息
    """
    if request.method == "POST":
        user = request.user
        member_info = json.loads(request.body)
        try:
            can_edit_prop_list = [
                "phone_number",
                "qq_number",
                "email_number",
                "wechat_number",
            ]
            kwargs = {prop: member_info[prop] for prop in can_edit_prop_list}
            Member.objects.filter(id=user.id).update(**kwargs)
            return JsonResponse(
                {"result": True, "message": "更新成功", "code": 201, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except IntegrityError or DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {"result": False, "message": "更新失败", "code": 412, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )


logger = logging.getLogger("root")


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


@is_teacher
def manage_course(request):
    # 增
    if request.method == "POST":
        req = json.loads(request.body)
        course_name = req.get("course_name")  # 想创建的课程名称
        teacher = req.get("teacher")
        course_introduction = req.get("course_introduction")  # 课程简介
        manage_student = req.get("manage_student")  # 学生管理员
        try:
            news_course_info = Course.objects.create(
                course_name=course_name,
                course_introduction=course_introduction,
                teacher=teacher,
                create_people="{}({})".format(
                    request.user.class_number, request.user.name
                ),
                manage_student=manage_student,
            )  # 将得到的数据加到course表
            UserCourseContact.objects.create(
                user_id=request.user.id, course_id=news_course_info.id
            )
            return JsonResponse(
                {"result": True, "message": "增加成功", "code": 201, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": True,
                    "message": "增加失败，请检查您输入的信息或者身份信息是否完善",
                    "code": 412,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )

    # 删
    if request.method == "DELETE":
        course_id = request.GET.get("course_id")
        if not course_id:
            return JsonResponse(
                {
                    "result": False,
                    "message": "删除失败！课程id不能为空",
                    "code": 400,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        try:
            with transaction.atomic():
                user_info = "{}({})".format(
                    request.user.class_number, request.user.name
                )
                course = Course.objects.get(id=course_id)
                if course.create_people == user_info or course.teacher == user_info:
                    course.delete()
                    UserCourseContact.objects.filter(course_id=course_id).delete()
                    return JsonResponse(
                        {
                            "result": True,
                            "message": "删除成功",
                            "code": 200,
                            "data": [],
                        },
                        json_dumps_params={"ensure_ascii": False},
                    )
                else:
                    return JsonResponse(
                        {
                            "result": False,
                            "message": "删除失败，权限不够",
                            "code": 403,
                            "data": [],
                        },
                        json_dumps_params={"ensure_ascii": False},
                    )
        except ObjectDoesNotExist as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "删除失败！",
                    "code": 412,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )

    # 改
    if request.method == "PUT":
        req = json.loads(request.body)
        course_id = req.pop("id", "")
        if not course_id:
            return JsonResponse(
                {
                    "result": False,
                    "message": "修改失败！课程id不能为空",
                    "code": 400,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        try:
            user_info = "{}({})".format(request.user.class_number, request.user.name)
            course = Course.objects.get(id=course_id)
            if course.create_people == user_info or course.teacher == user_info:
                for k, v in req.items():
                    setattr(course, k, v)
                course.save()
                return JsonResponse(
                    {"result": True, "message": "修改成功", "code": 200, "data": []},
                    json_dumps_params={"ensure_ascii": False},
                )
            else:
                return JsonResponse(
                    {
                        "result": False,
                        "message": "修改失败，权限不够",
                        "code": 403,
                        "data": [],
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "修改失败",
                    "code": 412,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )


# 查课程列表
def search_courses_by_userid(request):
    if request.method == "GET":
        course_ids = UserCourseContact.objects.filter(
            user_id=request.user.id
        ).values_list("course_id", flat=True)
        course = Course.objects.in_bulk(course_ids).values()
        courses = serializers.serialize("python", course, ensure_ascii=False)
        return JsonResponse(
            {
                "result": True,
                "message": "查询成功",
                "code": 200,
                "data": courses,
            },
            json_dumps_params={"ensure_ascii": False},
        )


# 下拉显示老师名称列表
def search_teacher_names(request):
    if request.method == "GET":
        try:
            teacher_names = []
            teachers = Member.objects.filter(identity="TEACHER")
            for teacher in teachers:
                teacher_names.append(
                    "{}({})".format(teacher.class_number, teacher.name)
                )
            return JsonResponse(
                {
                    "result": True,
                    "message": "显示成功",
                    "code": 200,
                    "data": json.dumps(teacher_names),
                },
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "显示异常",
                    "code": 400,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )


def verify_school_user(request):
    """
    功能：通过学分制的账号密码, 进行验证, 并绑定用户
    输入：request头中带有username,password
    返回：认证成功： result: True; data: user_id
         认证失败： result: False; data: []; message：错误信息
    """
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            result, user_info, message = identify_user(
                username=username, password=password
            )
            if result:
                user = Member.objects.filter(class_nnumber=username)
                user_id = user.values()[0].get("id")
                user.update(
                    class_number=user_info["user_name"],
                    name=user_info["user_real_name"],
                    professional_class=user_info["user_class"],
                    gender=Member.Gender.MAN
                    if user_info["user_sex"] == "男"
                    else Member.Gender.WOMAN,
                    identity=Member.Identity.STUDENT,
                    college=user_info["user_college"],
                )
                data = {
                    "result": True,
                    "message": message,
                    "code": 201,
                    "data": {
                        "user_id": user_id,
                    },
                }
                return JsonResponse(data)
            else:
                data = {"result": result, "message": message, "data": []}
                return JsonResponse(data)
        except Exception as e:
            data = {"result": False, "message": e, "code": 500, "data": []}  # 后端出错
            return JsonResponse(data)
