import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
import xlrd

from blueapps.core.exceptions import DatabaseError

from course.models import Member, UserCourseContact, Course

logger = logging.getLogger("root")


# 老师为指定课程导入学生信息
def import_student_excel(request):
    excel_files = request.FILES.get("excel_file")
    suffix = excel_files.name.split(".")[-1]
    course_id = request.POST.get("course_id")
    if suffix == "xls":
        data = xlrd.open_workbook(
            filename=None, file_contents=excel_files.read(), formatting_info=True
        )
    elif suffix == "xlsx":
        data = xlrd.open_workbook(filename=None, file_contents=excel_files.read())
    else:
        return JsonResponse(
            {
                "result": False,
                "message": "导入文件错误，请检查导入文件是否为excel格式",
                "code": 406,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )
    tables = data.sheets()
    row_sign = 0
    values_1 = []
    for table in tables:
        rows = table.nrows
        values_0 = table.row_values(0)
        if rows != 1:
            values_1 = table.row_values(1)
        try:
            if values_0[0] == "教学班点名册" and values_1[0] == "学年" and values_1[2] == "学期":
                with transaction.atomic():
                    for row in range(4, rows):
                        row_values = table.row_values(row)
                        err_sign = (row + 1)
                        defaults = {"username": row_values[0] + "{}".format("X"), "class_number": row_values[0],
                                    "name": row_values[2], "identity": "STUDENT",
                                    "professional_class": row_values[4]}
                        member_object, creat = Member.objects.update_or_create(
                            username=row_values[0] + "{}".format("X"),
                            class_number=row_values[0],  # 学号
                            name=row_values[2],  # 姓名
                            identity="STUDENT",
                            professional_class=row_values[4],  # 班级
                            defaults=defaults
                        )
                        UserCourseContact.objects.update_or_create(user_id=member_object.id, course_id=course_id)
                        row_sign = row_sign + 1
                return JsonResponse(
                    {
                        "result": True,
                        "message": "导入成功,导入{0}行数据".format(row_sign),
                        "code": 200,
                        "data": [],
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
        except Exception:
            return JsonResponse(
                {
                    "result": False,
                    "message": "文件导入错误，可能存在重复值，错误行{0}, 或者您的文件字段不匹配".format(row_sign),
                    "code": 200,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )


# 根具课程id为课程新加学生,根据传递参数可以新增一个或者多个
def add_course_student(request):
    req = json.loads(request.body)
    course_id = req.get("course_id")
    student_id = req.get("student")  # 前端传递一个学生id的列表
    if not course_id:
        return JsonResponse(
            {
                "result": False,
                "message": "增加失败，课程id不存在",
                "code": 403,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )
    for student in student_id:  # 遍历学生id列表创建关系
        UserCourseContact.objects.update_or_create(course_id=course_id, user_id=student)
    return JsonResponse(
        {
            "result": True,
            "message": "增加成功",
            "code": 200,
            "data": [],
        },
        json_dumps_params={"ensure_ascii": False},
    )


# 下载学生点名册模板
def download_student_excel_template(request):
    file = open('static/files/studentTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="studentTemplate.xls"'
    return response


# 获取学生列表
def search_course_student(request):
    req = json.loads(request.body)
    student_info = {}
    student = []
    course_id = req.get("course_id")
    if not course_id:
        return JsonResponse(
            {
                "result": False,
                "message": "课程id不能为空",
                "code": 406,
                "data": [],
            },
        )
    try:
        user_ids = UserCourseContact.objects.filter(course_id=course_id).values_list(
            "user_id", flat=True
        )
        for user_id in user_ids:
            user_objects = Member.objects.get(id=user_id)
            if user_objects.identity == "STUDENT":
                student_info["student"] = ("{0}({1})".format(user_objects.class_number, user_objects.name))
                student_info["student_id"] = user_objects.id
                student_info["id"] = user_objects.id
                student_info["name"] = user_objects.name
                student_info["class_number"] = user_objects.class_number
                student_info["professional_class"] = user_objects.professional_class
                student.append(student_info.copy())
        return JsonResponse(
            {
                "result": True,
                "message": "成功",
                "code": 200,
                "data": student,
            },
            json_dumps_params={"ensure_ascii": False},
        )
    except DatabaseError:
        return JsonResponse(
            {
                "result": False,
                "message": "获取失败",
                "code": 400,
                "data": student,
            },
            json_dumps_params={"ensure_ascii": False},
        )


# 删除学生（删除对应学生与课程关系）
def delete_student_course_contact(request):
    if request.method == "DELETE":
        course_id = request.GET.get("course_id")
        user_class_number = request.GET.get("user_class_number")    # 前端给我传值没有student_id，那会为了实现接口,只能通过学号查找
        # 我本来的想法
        # student_id = request.GET.get("student_id")
        # UserCourseContact.objects.get(course_id=course_id, user_id=student_id).delete()
        user_object = Member.objects.get(class_number=user_class_number)
        try:
            UserCourseContact.objects.get(course_id=course_id, user_id=user_object.id).delete()
            return JsonResponse(
                {"result": True, "message": "删除成功", "code": 200, "data": []},
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
