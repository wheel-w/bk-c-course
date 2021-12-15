from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Member, UserCourseContact

# Create your views here.


def is_teacher(fun):
    def inner(request, *args, **kwargs):
        try:
            userName = request.user.username
            identity = Member.objects.filter(username=userName).values(
                "identity"
            )  # 取出数据表中的identity值
            if (
                identity.first()["identity"] == Member.Identity.TEACHER
            ):  # 将取出的Queryset转化为字典与字符串比较
                return fun(request, *args, **kwargs)
            else:
                return JsonResponse(
                    {"result": False, "code": -1, "message": "您没有操作权限", "data": []}
                )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "code": -1, "message": "请求错误！", "data": []}
            )  # 返回信息

    return inner


@csrf_exempt
@is_teacher
def manage_course(request):
    # 增
    if request.method == "POST":
        try:
            userName = request.user.username  # 获取当前登录用户的名称
            courseName = request.POST.get("courseName", "未添加")  # 想创建的课程名称
            courseIntroduction = request.POST.get("courseIntroduction", "")  # 课程简介
            teacher = request.POST.get("teacher", userName)  # 授课教师
            manageStudent = request.POST.get("manageStudent", "")  # 学生管理员
            Course.objects.create(
                course_name=courseName,
                course_introduction=courseIntroduction,
                teacher=teacher,
                create_people=userName,
                manage_student=manageStudent,
            )  # 将得到的数据加到course表
            return JsonResponse(
                {"result": True, "message": "增加成功", "code": 200, "date": []}
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "message": "增加失败，请查看您输入的信息", "code": 400, "date": []}
            )
    # 删
    elif request.method == "DELETE":
        try:
            req = QueryDict(request.body)
            courseId = req.get("courseId")
            Course.objects.filter(id=courseId).delete()
            return JsonResponse(
                {"result": True, "message": "删除成功", "code": 200, "date": []}
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "message": "删除失败，请核对您输入的信息", "code": 400, "date": []}
            )
    # 查
    if request.method == "GET":
        try:
            userName = request.user.username
            userId = Member.objects.get(username=userName).id
            courseIds = UserCourseContact.objects.filter(user_id=userId).values_list(
                "course_id", flat=True
            )
            courseNames = Course.objects.in_bulk(courseIds).values()
            courseName = serializers.serialize("json", courseNames, ensure_ascii=False)
            return JsonResponse(
                {
                    "result": True,
                    "message": "查询成功",
                    "code": 200,
                    "id": userId,
                    "data": courseName,
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "message": "用户不存在", "code": 404, "data": []}
            )
    # 改
    if request.method == "PUT":
        req = QueryDict(request.body)
        try:
            if len(str(req.get("courseId"))) == 0:
                return JsonResponse(
                    {"result": False, "message": "课程id不能为空", "code": 415, "data": []},
                    json_dumps_params={"ensure_ascii": False},
                )
            else:
                courseId = req.get("courseId")
                course = Course.objects.get(id=courseId)
                courseName = req.get("courseName", course.course_name)
                courseIntroduction = req.get(
                    "courseIntroduction", course.course_introduction
                )
                teacher = req.get("teacher", course.teacher)
                manageStudent = req.get("manageStudent", Course.manage_student)
                Course.objects.filter(id=courseId).update(
                    course_name=courseName,
                    course_introduction=courseIntroduction,
                    teacher=teacher,
                    manage_student=manageStudent,
                )
                new_course = serializers.serialize(
                    "json", Course.objects.filter(id=courseId), ensure_ascii=False
                )
                return JsonResponse(
                    {
                        "result": True,
                        "message": "修改成功",
                        "code": 200,
                        "data": new_course,
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"result": False, "message": "错误异常", "code": 415, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
