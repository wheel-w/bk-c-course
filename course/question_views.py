import json
import logging

import xlrd
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import FileResponse, JsonResponse

from blueapps.core.exceptions import DatabaseError

from .models import Chapter, Course, Question

logger = logging.getLogger("root")


# 出题操作权限装饰器
def set_question_rights(fun):
    def inner(request, *args, **kwargs):
        if request.method == "DELETE":
            course_id = request.GET.get("course_id")
        else:
            req = json.loads(request.body)
            course_id = req.get("course_id")
        user_info = "{}({})".format(request.user.class_number, request.user.name)
        try:
            course = Course.objects.get(id=course_id)
            if course.create_people == user_info or course.teacher == user_info:
                return fun(request, *args, **kwargs)
            else:
                return JsonResponse(
                    {"result": False, "code": 403, "message": "您没有操作权限！", "data": []}
                )
        except ObjectDoesNotExist as e:
            logger.exception(e)
            return JsonResponse(
                {"result": False, "code": 401, "message": "请求错误！课程id不存在", "data": []}
            )  # 返回信息

    return inner


# 获取章节列表
def get_chapter_list(request):
    if request.method == "GET":
        chapter_list = []
        course_id = request.GET.get("course_id")  # 通过路由传course_id
        if not course_id:
            return JsonResponse(
                {
                    "result": False,
                    "message": "课程id不能为空",
                    "code": 406,
                    "data": [],
                },
            )
        chapters = Chapter.objects.filter(course_id=course_id)
        for chapter in chapters:
            chapter_list.append(
                {"chapter_id": chapter.id, "chapter_name": chapter.chapter_name}
            )
        return JsonResponse(
            {
                "result": True,
                "message": "显示成功",
                "code": 200,
                "data": chapter_list,
            },
            json_dumps_params={"ensure_ascii": False},
        )


# 章节的批量增删改
@set_question_rights
def operate_chapter(request):
    if request.method == "POST":
        req = json.loads(request.body)
        course_id = req.get("course_id")
        # 获取数据库存在的课程章节
        existing_chapter_dict = Chapter.objects.filter(course_id=course_id).values_list(
            "id", flat=True
        )
        new_chapter_list = []  # 新增章节列表
        update_chapter_list = []  # 更新操作的章节列表
        update_chapter_id_list = []  # 更新操作的章节id
        # 获取前端传入的当前章节列表
        current_chapter_list = req.get("chapter_list")
        for current_chapter in current_chapter_list:
            if "id" in current_chapter:
                update_chapter_id_list.append(current_chapter["id"])
                update_chapter_list.append(Chapter(**current_chapter))
            else:
                obj = Chapter(
                    course_id=course_id, chapter_name=current_chapter["chapter_name"]
                )
                new_chapter_list.append(obj)
        del_id_list = list(
            set(existing_chapter_dict) - set(update_chapter_id_list)
        )  # 删除章节id列表
        try:
            with transaction.atomic():
                Chapter.objects.filter(id__in=del_id_list).delete()  # 批量删除
                Chapter.objects.bulk_update(
                    update_chapter_list, ["chapter_name"]
                )  # 批量更新
                Chapter.objects.bulk_create(new_chapter_list)  # 批量创建数据
            return JsonResponse(
                {
                    "result": True,
                    "message": "操作成功",
                    "code": 200,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "操作失败！",
                    "code": 412,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
    else:
        return JsonResponse(
            {
                "result": False,
                "message": "请求方法错误",
                "code": 400,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )


TYPES_DICT = {
    "单选题": "SINGLE",
    "多选题": "MULTIPLE",
    "填空题": "COMPLETION",
    "判断题": "JUDGE",
    "简答题": "SHORT_ANSWER",
}


# 老师为指定课程导入问题信息
@set_question_rights
def import_question_excel(request):
    excel_files = request.FILES.get("excel_file")
    suffix = excel_files.name.split(".")[-1]
    course_id = request.POST.get("course_id")
    chapter_id = request.POST.get("chapter_id")
    if suffix == "xls":
        data = xlrd.open_workbook(filename=None, file_contents=excel_files.read())
    else:
        return JsonResponse(
            {
                "result": False,
                "message": "导入文件错误，请检查导入文件是否为excel后缀名（.xls）格式",
                "code": 406,
                "data": [],
            },
            json_dumps_params={"ensure_ascii": False},
        )
    table = data.sheet_by_index(0)
    question_info = {}
    question_info_list = []
    question_list = []
    row_sign = 0
    rows = table.nrows
    values_0 = table.row_values(0)
    if rows != 1:
        if not (values_0[0] == "questType" and values_0[1] == "questTitle"):
            return JsonResponse(
                {
                    "result": False,
                    "message": "文件格式错误,请检查文件内容是否符合模板规范",
                    "code": 403,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        for row in range(1, rows):
            row_values = table.row_values(row)
            question_info["types"] = TYPES_DICT[row_values[0]]
            question_info["question"] = row_values[1]
            question_info["option_A"] = row_values[3]
            question_info["option_B"] = row_values[4]
            question_info["option_C"] = row_values[5]
            question_info["option_D"] = row_values[6]
            question_info["option_E"] = row_values[7]
            question_info["answer"] = row_values[2]
            question_info["explain"] = row_values[8]
            question_info_list.append(question_info.copy())
            row_sign = row_sign + 1
        chapter_object = Chapter.objects.filter(id=chapter_id, course_id=course_id)
        if not chapter_object:
            return JsonResponse(
                {
                    "result": False,
                    "message": "章节不存在",
                    "code": 406,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        for content in question_info_list:
            if content["types"] == "COMPLETION" and ("()" not in content["question"] and "（）" not in content["question"]):
                pass
            else:
                question_list.append(
                    Question(
                        course_id=course_id,
                        chapter_id=chapter_id,
                        types=content["types"],
                        question=content["question"],
                        option_A=content["option_A"],
                        option_B=content["option_B"],
                        option_C=content["option_C"],
                        option_D=content["option_D"],
                        option_E=content["option_E"],
                        answer=content["answer"],
                        explain=content["explain"],
                    )
                )
        Question.objects.bulk_create(question_list)
        return JsonResponse(
            {
                "result": True,
                "message": "导入成功,共导入{}行数据".format(row_sign),
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


# 出题模板下载
def download_set_question_excel_template(request):
    file = open("static/files/setQuestionTemplate.xls", "rb")
    response = FileResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = 'attachment;filename="setQuestionTemplate.xls"'
    return response


#  展示这个课程的所有章节的所有题目， 也就是题目的查询
def get_question_list(request):
    if request.method == "GET":
        question_list = []
        course_id = request.GET.get("course_id")  # 通过路由传course_id
        chapter_id = request.GET.get("chapter_id")
        if chapter_id:
            questions = Question.objects.filter(chapter_id=chapter_id)
        else:
            if not course_id:
                return JsonResponse(
                    {
                        "result": False,
                        "message": "课程id不能为空",
                        "code": 406,
                        "data": [],
                    },
                )
            questions = Question.objects.filter(course_id=course_id)
        for question in questions:
            question_list.append(
                {
                    "question_id": question.id,
                    "chapter_id": question.chapter_id,
                    "types": question.types,
                    "question": question.question,
                    "option_A": question.option_A,
                    "option_B": question.option_B,
                    "option_C": question.option_C,
                    "option_D": question.option_D,
                    "option_E": question.option_E,
                    "answer": question.answer,
                    "explain": question.explain,
                }
            )
        return JsonResponse(
            {
                "result": True,
                "message": "显示成功",
                "code": 200,
                "data": question_list,
            },
            json_dumps_params={"ensure_ascii": False},
        )


# 问题的增删改
@set_question_rights
def teacher_set_question(request):
    # 增
    if request.method == "POST":
        req = json.loads(request.body)
        question_type = req.get("types")
        question_type_value = TYPES_DICT[question_type]
        chapter_id = req.get("chapter_id")
        course_id = req.get("course_id")
        question = req.get("question")
        option_A = req.get("option_A", "")
        option_B = req.get("option_B", "")
        option_C = req.get("option_C", "")
        option_D = req.get("option_D", "")
        option_E = req.get("option_E", "")
        answer = req.get("answer")
        explain = req.get("explain", "")
        try:
            Question.objects.create(
                course_id=course_id,
                question=question,
                chapter_id=chapter_id,
                types=question_type_value,
                option_A=option_A,
                option_B=option_B,
                option_C=option_C,
                option_D=option_D,
                option_E=option_E,
                answer=answer,
                explain=explain,
            )
            return JsonResponse(
                {"result": True, "message": "出题成功", "code": 201, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "出题失败，请检查您输入的信息是否符合规范",
                    "code": 412,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
    # 删
    if request.method == "DELETE":
        question_id_list = json.loads(request.GET.get("question_id_list"))  # 可以传递多个问题id
        try:
            Question.objects.filter(id__in=question_id_list).delete()
            return JsonResponse(
                {
                    "result": True,
                    "message": "删除成功",
                    "code": 200,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "删除失败",
                    "code": 403,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
    # 改
    if request.method == "PUT":
        req = json.loads(request.body)
        question_id = req.pop("question_id", "")
        if not question_id:
            return JsonResponse(
                {
                    "result": False,
                    "message": "修改失败！问题id不能为空",
                    "code": 400,
                    "data": [],
                },
                json_dumps_params={"ensure_ascii": False},
            )
        try:
            question = Question.objects.get(id=question_id)
            for k, v in req.items():
                setattr(question, k, v)
            question.save()
            return JsonResponse(
                {"result": True, "message": "修改成功", "code": 200, "data": []},
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
