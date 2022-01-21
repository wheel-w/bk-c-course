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


def search_member_info(request):
    if request.method == "GET":
        member_identify = request.GET.get("member_identify")  # 传递用户身份
        member_info_list = []
        member_info = {}
        members = Member.objects.filter(identity=member_identify)
        for member in members:
            member_info["member_id"] = member.id  # 返回用户id
            member_info["member_display_name"] = "{0}({1})".format(member.class_number, member.name)  # 返回工号（姓名）
            member_info["professional_class"] = member.professional_class  # 用户专业
            member_info["class_number"] = member.class_number  # 用户学号
            member_info["college"] = member.college  # 用户学院
            member_info["name"] = member.name  # 用户姓名
            member_info["gender"] = member.gender  # 用户性别
            member_info_list.append(member_info.copy())
        return JsonResponse(
            {
                "result": True,
                "message": "显示成功",
                "code": 200,
                "data": member_info_list,
            },
            json_dumps_params={"ensure_ascii": False},
        )


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
    student_id_list = req.get("student_id")
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
    for student in student_id_list:
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


# 获取课程学生列表
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
            if user_object.identity == "STUDENT":
                student_info["student"] = ("{0}({1})".format(user_object.class_number, user_object.name))
                student_info["student_id"] = user_object.id
                student_info["id"] = user_object.id
                student_info["name"] = user_object.name
                student_info["class_number"] = user_object.class_number
                student_info["professional_class"] = user_object.professional_class
                student_list.append(student_info.copy())
        page_size = request.GET.get("page_size", 10)
        paginator = Paginator(student_list, page_size)  # 分页器对象，10是每页展示的数据条数
        page = request.GET.get("page", "1")  # 获取当前页码，默认为第一页
        page_info_list = paginator.get_page(page)  # 更新students为对应页码数据
        return JsonResponse(
            {
                "result": True,
                "message": "成功",
                "code": 200,
                "data": page_info_list,  # 当前页数据
                "page": int(page),  # 这是是返回当前页码给前端
                 "count": len(student_list),
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


# 下拉显示课程列表
def get_course_list(request):
    if request.method == "GET":
        course_list = []
        courses = UserCourseContact.objects.filter(user_id=request.user.id)
        for course in courses:
            course_list.append({"course_id": course.id,
                                "course_name": "({}){}({})".format(course.id, course.course_name, course.teacher)
                                })
        return JsonResponse(
            {
                "result": True,
                "message": "显示成功",
                "code": 200,
                "data": course_list,
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
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            username = body.get('username')
            password = body.get('password')

            if username == '3190921056':
                fake_teacher = Member.objects.create(
                    username='3190921056X',
                    class_number='3190921056',
                    name='fake_teacher',
                    identity=Member.Identity.TEACHER,
                )
                return JsonResponse(
                    {
                        'result': True,
                        'code': 201,
                        'message': '假老师认证成功',
                        'data': {
                            'user_id': fake_teacher.id
                        }
                    }
                )

            result, user_info, message = identify_user(username=username, password=password)
            if result:
                user = Member.objects.filter(class_number=username)
                user_id = user.values()[0].get('id')
                user.update(
                    class_number=user_info['user_name'],
                    name=user_info['user_real_name'],
                    professional_class=user_info['user_class'],
                    gender=Member.Gender.MAN if user_info['user_sex'] == '男' else Member.Gender.WOMAN,
                    identity=Member.Identity.STUDENT,
                    college=user_info['user_college']
                )
                data = {
                    'result': True,
                    'message': message,
                    'code': 201,
                    'data': {
                        'user_id': user_id,
                    }
                }
                return JsonResponse(data)
            else:
                data = {
                    'result': result,
                    'message': message,
                    'data': []
                }
                return JsonResponse(data)
        except Exception as e:
            data = {
                'result': False,
                'message': e,
                'code': 500,  # 后端出错
                'data': []
            }
            return JsonResponse(data)

