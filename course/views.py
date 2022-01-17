import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
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
    if suffix in ["xls", "xlsx"]:
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
    student_class_number = set()
    student_info_list = []
    student_member_list = []
    student_contact_list = []
    student_info = {}
    row_sign = 0
    for table in tables:
        rows = table.nrows
        values_0 = table.row_values(0)
        if rows != 1:
            values_1 = table.row_values(1)
            if not (values_0[0] == "教学班点名册" and values_1[0] == "学年"):
                return JsonResponse(
                    {
                        "result": False,
                        "message": "文件格式错误,请检查文件内容是否符合模板规范",
                        "code": 403,
                        "data": [],
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
            else:
                for row in range(4, rows):
                    row_values = table.row_values(row)
                    student_info["class_number"] = row_values[0]
                    student_info["professional_class"] = row_values[4]
                    student_info["name"] = row_values[2]
                    student_info_list.append(student_info.copy())
                    student_class_number.add(row_values[0])
                user_class_number = Member.objects.filter(class_number__in=student_class_number).values_list(
                    "class_number", flat=True)
                user_ids = UserCourseContact.objects.filter(course_id=course_id).values_list("user_id", flat=True)
                user_ids_list = list(user_ids)
                user_class_number_list = list(user_class_number)
                for student in student_info_list:
                    if student["class_number"] not in user_class_number_list:
                        student_member_list.append(Member(username="{}X".format(student["class_number"]),
                                                          class_number=student["class_number"],
                                                          name=student["name"],
                                                          professional_class=student["professional_class"]))
                Member.objects.bulk_create(student_member_list)
                objs = Member.objects.filter(class_number__in=student_class_number).values_list(
                    "id", flat=True)
                objs_list = list(objs)
                for obj in objs_list:
                    if obj not in user_ids_list:
                        student_contact_list.append(UserCourseContact(user_id=obj, course_id=course_id))
                        row_sign = row_sign + 1
                UserCourseContact.objects.bulk_create(student_contact_list)
                return JsonResponse(
                    {
                        "result": True,
                        "message": "导入成功,共导入{0}行数据".format(row_sign),
                        "code": 200,
                        "data": [],
                    },
                    json_dumps_params={"ensure_ascii": False},
                )
        return JsonResponse(
            {
                "result": False,
                "message": "请检查您的excel表中的数据是否齐全",
                "code": 403,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )


# 根具课程id为课程新加学生
def add_course_student(request):
    req = json.loads(request.body)
    course_id = req.get("course_id")
    student_id = req.get("student_id")
    student_list = []
    if not course_id:
        return JsonResponse(
            {
                "result": False,
                "message": "增加失败，课程id不存在",
                "code": 406,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )
    user_ids = UserCourseContact.objects.filter(course_id=course_id).values_list("user_id", flat=True)
    user_ids_list = list(user_ids)
    for student in student_id:
        if student not in user_ids_list:
            student_list.append(UserCourseContact(user_id=student, course_id=course_id))
    if not student_list:
        return JsonResponse(
            {
                "result": False,
                "message": "增加失败，请勿重复添加关系",
                "code": 403,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )
    UserCourseContact.objects.bulk_create(student_list)
    return JsonResponse(
        {
            "result": True,
            "message": "增加成功, 已经去除重复关系",
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
    student_info = {}
    student_list = []
    course_id = request.GET.get("course_id")
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
        user_ids_list = list(user_ids)
        user_objects = Member.objects.in_bulk(user_ids_list)
        for user_object in user_objects:
            if user_objects.identity == "STUDENT":
                student_info["student"] = ("{0}({1})".format(user_object.class_number, user_object.name))
                student_info["student_id"] = user_object.id
                student_info["id"] = user_object.id
                student_info["name"] = user_object.name
                student_info["class_number"] = user_object.class_number
                student_info["professional_class"] = user_object.professional_class
                student_list.append(student_info.copy())
        paginator = Paginator(student_list, 10)  # 分页器对象，10是每页展示的数据条数
        page = request.GET.get("page", "1")  # 获取当前页码，默认为第一页
        student_list_page = paginator.get_page(page)  # 更新students为对应页码的10条数据
        return JsonResponse(
            {
                "result": True,
                "message": "成功",
                "code": 200,
                "data": student_list_page,
                "page": json.dumps(int(page)),  # 这是是返回当前页码给前端
                "page_range": list(paginator.page_range),  # 这个参数是告诉前端一共有多少页
                "number": len(student_list),
                "student_list": student_list,
            },
            json_dumps_params={"ensure_ascii": False},
        )
    except DatabaseError:
        return JsonResponse(
            {
                "result": False,
                "message": "获取失败",
                "code": 400,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )


# 删除学生（删除对应学生与课程关系）
def delete_student_course_contact(request):
    if request.method == "DELETE":
        course_id = request.GET.get("course_id")
        student_id = request.GET.get("student_id")  # 传递学生id列表
        try:
            UserCourseContact.objects.filter(user_id__in=student_id, course_id=course_id).delete()
            return JsonResponse(
                {"result": True, "message": "删除成功", "code": 200, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except ObjectDoesNotExist as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "删除失败！,课程号不存在",
                    "code": 412,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
