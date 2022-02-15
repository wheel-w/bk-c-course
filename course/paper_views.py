import json
import logging

from MySQLdb import DatabaseError
from django.contrib.auth import login
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

from .models import CustomType, Member, Paper, PaperQuestionContact, Question, StudentAnswer
from .views import is_teacher
from .celery_task.judge_objective import judge_objective

logger = logging.getLogger("root")


@is_teacher
def question_title(request):
    method = request.method

    if method == 'POST':
        """
        功能：针对每一种的课程，建立大题标题
        输入：课程id， 大题题目
        返回：添加成功或失败
        """
        body = json.loads(request.body)
        course_id = body.get('course_id')
        custom_type_info = body.get('custom_type_info')
        if custom_type_info is None or course_id is None:
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })
        create_types = []
        update_types = []
        delete_types = []

        for info in custom_type_info:
            if info.get('custom_type_id') is None:
                create_types.append(CustomType(course_id=course_id, custom_type_name=info.get('custom_type_name')))
            elif info.get('custom_type_name') is None:
                delete_types.append(info.get('custom_type_id'))
            else:
                update_types.append(CustomType(
                    custom_type_name=info.get('custom_type_name'),
                    id=info.get('custom_type_id')
                ))
        try:
            with transaction.atomic():
                CustomType.objects.bulk_create(create_types)
                CustomType.objects.bulk_update(update_types, ['custom_type_name'])
                CustomType.objects.filter(id__in=delete_types).delete()
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'message': '保存失败',
                'code': 500,
                'data': {}
            })
        return JsonResponse({
            'result': True,
            'message': '保存成功',
            'code': 200,
            'data': {}
        })

    if method == 'GET':
        """
        功能: 根据课程id，返回对应的大题的信息
        输入: course_id
        返回: 该课程的题目信息
        """
        course_id = request.GET.get('course_id')
        if course_id is None:
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })

        try:
            custom_types = list(CustomType.objects.filter(course_id=course_id).values())
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse({
                'result': True,
                'code': 500,
                'message': '查询失败(请检查日志)',
                'date': {}
            })

        return JsonResponse({
            'result': True,
            'code': 200,
            'message': '查询成功',
            'data': {
                'custom_types': custom_types
            }
        })

    else:
        return JsonResponse({
            'result': False,
            'code': 405,
            'message': '请求方法错误'
        })


def paper(request):
    method = request.method

    if method == "GET":
        """
        功能: 
             老师
             1. 根据老师id，返回给老师的所有卷子                       
             2. 根据老师id与课程id，返回对应老师教的本门课程的所有卷子     
             3. 根据question_id查询所含该题目的卷子（同步题目使用）      
             学生
             1. 根据课程去查                                  
             附加
             1. 根据question_id查询包含该题的卷子                
                        
        输入：老师id或老师与课程id
        返回：对应卷子信息
        """
        question_id = request.GET.get('question_id')
        query_param = {}
        identity = request.user.identity
        if not question_id:
            if identity == Member.Identity.TEACHER:
                query_param = {'teacher': str(Member.objects.get(id=request.user.id))}
            if identity == Member.Identity.STUDENT and not request.GET.get('course_id'):
                return JsonResponse({'result': False, 'code': 403, 'message': '请求参数不完整', 'data': {}})
            if identity == Member.Identity.STUDENT:
                query_param = {'status__in': ['RELEASE', 'MARKED']}
            if request.GET.get('course_id'):
                query_param['course_id'] = request.GET.get('course_id')
            if question_id:
                query_param['id__in'] = [pq.paper_id for pq in
                                         PaperQuestionContact.objects.filter(question_id=question_id)]
        else:
            query_param['id__in'] = [pq.paper_id for pq in
                                     PaperQuestionContact.objects.filter(question_id=question_id)]

        try:

            paper_info = list(Paper.objects.filter(**query_param).values())
            [p.pop('question_order') for p in paper_info]

        except Exception as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'message': '查询失败(请检查日志)',
                'code': 500,
                'data': {}
            })
        return JsonResponse({
            'result': True,
            'message': '查询成功',
            'code': 200,
            'data': paper_info
        })

    # 以下的方法只可以以老师的身份请求
    if request.user.identity != Member.Identity.TEACHER:
        return JsonResponse({
            'result': False,
            'code': 403,
            'message': '您没有操作权限！',
            'data': {}
        })

    if method == "POST":
        """
        功能：卷子的增加
        输入：试卷类型，课程id，卷子名称，教师信息
        返回：卷子id
        """
        body = json.loads(request.body)
        paper_info_list = [
            'types',
            'course_id',
            'chapter_id',
            'paper_name',
            'teacher'
        ]
        paper_info = {info: body.get(info) for info in paper_info_list}

        paper_info['teacher'] = str(Member.objects.get(id=request.user.id))
        # 当创建卷子的那一刻（还没有给卷子选题），将卷子状态设置为”草稿“
        paper_info['status'] = Paper.Status.DRAFT
        if None in paper_info.values():
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })

        try:
            paper = Paper.objects.create(**paper_info)
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'message': '添加卷子失败(请检查日志)',
                'code': 500,
                'data': {}
            })

        return JsonResponse({
            'result': True,
            'message': '添加卷子成功',
            'code': 200,
            'data': {
                'paper_id': paper.id
            }
        })

    if method == "DELETE":
        """
        功能：删除对应卷子
        输入：对应卷子id
        返回：是否成功
        """

        body = json.loads(request.body)
        paper_id = body.get('paper_id')
        if paper_id is None:
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })

        try:
            paper = Paper.objects.filter(id=paper_id)
            if not paper:
                return_data = {'result': False, 'message': '删除失败(数据库中没有该字段)', 'code': 412, 'data': {}}
            else:
                if paper.get().status != Paper.Status.DRAFT:
                    return_data = {'result': False, 'message': '卷子不可以删除（只有草稿卷才可以删除）', 'code': 412, 'data': {}}
                else:
                    result = paper.delete()[0]
                    if result:
                        question_num = PaperQuestionContact.objects.filter(paper_id=paper_id).delete()[0]
                        return_data = {'result': True,
                                       'message': '删除成功(关联题目{}道)'.format(question_num),
                                       'code': 200, 'data': {}}
                    else:
                        return_data = {'result': False, 'message': '删除失败(数据库中没有该字段)', 'code': 412, 'data': {}}

        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'message': '删除卷子失败(请检查日志)',
                'code': 500,
                'data': {}
            })

        return JsonResponse(return_data)

    if method == "PUT":
        """
        功能：卷子信息的修改(所有属性)
        输入：卷子id与修改信息与对应的值
        返回：是否成功
        """
        body = json.loads(request.body)
        paper_id = body.get('paper_id')
        update_info = body.get('update_info')
        # 起始时间同时设定
        if paper_id is None or (('start_time' in update_info.keys()) ^ ('end_time' in update_info.keys())):
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })
        if ('status' in update_info.keys()) and (update_info.get('status') not in Paper.status_list):
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '卷子状态码不存在',
                'data': {}
            })
        try:
            result = Paper.objects.filter(id=paper_id).update(**update_info)
            if result:
                return_data = {'result': True, 'message': '修改成功', 'code': 200,
                               'data': {'paper_id': paper_id, 'update_info': update_info}}
            else:
                return_data = {'result': False, 'message': '修改失败(数据库中没有该字段)', 'code': 412, 'data': {}}

        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'message': '卷子信息修改失败(请检查日志)',
                'code': 500,
                'data': {}
            })

        return JsonResponse(return_data)

    else:
        return JsonResponse({
            'result': False,
            'code': 405,
            'message': '请求方法错误'
        })


def manage_paper_question_contact(request):
    if request.method == "GET":
        """
        功能: 查询卷子对应的习题
        输入: 对应卷子的id
        返回: 卷子信息
             {
                titles: { 
                        '大题题目id': '大题题目内容'
                        },
                questions: {
                        '大题题目id' : [题目信息列表]
                        }
             }
        """
        paper_id = request.GET.get('paper_id')
        identity = request.user.identity
        flag = None

        if paper_id is None or (identity == Member.Identity.TEACHER and request.GET.get('flag') is None):
            return JsonResponse({'result': False, 'code': 400, 'message': '请求参数不完整', 'data': {}})
        elif identity == Member.Identity.TEACHER:
            flag = int(request.GET.get('flag'))

        try:
            paper = Paper.objects.get(id=paper_id)
            if identity == Member.Identity.STUDENT and paper.status == Paper.Status.DRAFT:
                return JsonResponse({'result': False, 'code': 403, 'message': '没有权限看查', 'dat': {}})

            order = json.loads(paper.question_order)
            custom_type_ids = order.keys()
            student_answer = None

            # 初始化传输题目的格式
            questions = {pq['id']: pq for pq in PaperQuestionContact.objects.filter(paper_id=paper_id).values()}
            question_data = {
                'titles': {i.id: i.custom_type_name for i in CustomType.objects.filter(id__in=custom_type_ids)},
                'questions': {i: [] for i in custom_type_ids}}

            # 分情况判断是否需要查询StudentAnswer表
            # 当老师请求此接口, flag==1，表示老师批改卷子；flag==0，表示老师预览卷子或继续出题
            if (identity == Member.Identity.TEACHER and flag == 1) or identity == Member.Identity.STUDENT:
                if identity == Member.Identity.TEACHER and \
                        (paper.end_time > timezone.now() or paper.status == Paper.Status.DRAFT):
                    return JsonResponse({'result': False, 'code': 403, 'message': '无法批改', 'data': {}})
                if paper.status != Paper.Status.DRAFT and paper.end_time < timezone.now():
                    student_answer = {}
                    query_param = {'PQContact_id__in': questions.keys()}
                    if identity == Member.Identity.STUDENT:
                        query_param['student_id'] = request.user.id
                    if identity == Member.Identity.TEACHER and request.GET.get('student_id'):
                        query_param['student_id'] = request.GET.get('student_id')
                    for sa in StudentAnswer.objects.filter(**query_param).values():
                        if paper.status != Paper.Status.MARKED:
                            sa.pop('score')
                        if sa['PQContact_id'] in student_answer.keys():
                            student_answer[sa['PQContact_id']].append(sa)
                        else:
                            student_answer[sa['PQContact_id']] = [sa]

        except Exception as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'code': 500,
                'message': '查询失败(请检查日志)',
                'date': {}
            })

        # 构造给前端传输的数据格式
        for title_id, question_ids in order.items():
            for q_id in question_ids:
                q = questions[q_id]
                if identity == Member.Identity.STUDENT and not student_answer:
                    q.pop('answer')
                    q.pop('explain')
                if student_answer:
                    q['student_answer'] = student_answer[q_id]
                question_data['questions'][title_id].append(q)

        return JsonResponse(
            {
                "result": True,
                "message": "查询成功",
                "code": 201,
                "data": question_data
            },
            json_dumps_params={"ensure_ascii": False},
        )

    # 以下的方法只可以以老师的身份请求
    if request.user.identity != Member.Identity.TEACHER:
        return JsonResponse({
            'result': False,
            'code': 403,
            'message': '您没有操作权限！',
            'data': {}
        })

    if request.method == 'POST':
        """
        功能: 保存卷子信息
        输入: 卷子与对应题目的信息
             {'大题题目id': [[小题id数组], [小题分数数组]]}
        返回: 保存成功或保存失败
        """
        body = json.loads(request.body)
        paper_info_list = body.get('paper_info')
        paper_id = body.get('paper_id')

        if paper_id is None or paper_info_list is None:
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })

        PQContact_info = ['types', 'question', 'option_A', 'option_B',
                          'option_C', 'option_D', 'option_E', 'answer', 'explain']
        question_id_list, score_list, create_obj_list, title_info = [], [], [], []

        for info_dict in paper_info_list:
            for k, v in info_dict.items():
                question_id_list.extend(v[0])
                score_list.extend(v[1])
                title_info.append((k, len(v[1])))
        try:
            # 通过小题的id在题库中将所有小题的信息拿出来
            for question in Question.objects.filter(id__in=question_id_list):
                PQContact = PaperQuestionContact(**({info: getattr(question, info) for info in PQContact_info}))
                PQContact.question_id = question.id
                PQContact.paper_id = paper_id
                PQContact.score = score_list[question_id_list.index(question.id)]
                create_obj_list.append(PQContact)

            with transaction.atomic():
                # 删除上一次的信息，将本次的题目数据进行添加
                PaperQuestionContact.objects.filter(paper_id=paper_id).delete()
                PaperQuestionContact.objects.bulk_create(create_obj_list)

                # 构造Json数据(顺序不能变)
                for PQContact in PaperQuestionContact.objects.filter(paper_id=paper_id):
                    score_list[question_id_list.index(PQContact.question_id)] = PQContact.id

            sum = 0
            order_json = {}
            for title in title_info:
                order_json[title[0]] = score_list[sum:sum + title[1]]
                sum += title[1]

            Paper.objects.filter(id=paper_id).update(question_order=json.dumps(order_json))

        except Exception as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'code': 500,
                'message': '保存失败(请检查日志)',
                'date': {}
            })

        return JsonResponse({
            'result': True,
            'code': 200,
            'message': '保存成功',
            'data': {}
        })

    # 编辑习题 单个编辑
    if request.method == "PUT":
        req = json.loads(request.body)
        PQ_contact_id = req["PQ_contact_id"]
        can_edit_prop_list = [
            "custom_type_id", "types", "score", "question", "option_A", "option_B", "option_C", "option_D",
            "option_E", "answer", "explain"
        ]
        kwargs = {key: req[key] for key in can_edit_prop_list}
        try:
            PaperQuestionContact.objects.filter(id=PQ_contact_id).update(**kwargs)
            return JsonResponse(
                {"result": True, "message": "更新成功", "code": 201, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {"result": False, "message": "更新失败", "code": 412, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
    else:
        return JsonResponse({
            'result': False,
            'code': 405,
            'message': '请求方法错误',
            'data': {}
        })


@is_teacher
def synchronous_paper(request):
    if request.method == "PUT":
        """
        功能: 同步题库与卷子中的题目
        输入: 卷子id（列表）（可以更新多个卷子）
             题目id
        返回: 成功或失败
        """
        req = json.loads(request.body)
        paper_id_list = req["paper_id"]
        question_id = req["question_id"]
        if paper_id_list is None or question_id is None:
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整',
                'data': {}
            })
        try:
            q = Question.objects.filter(id=question_id)
            PaperQuestionContact.objects.filter(paper_id__in=paper_id_list, question_id=question_id).update(
                question_id=q.values()[0].get('id'),
                question=q.values()[0].get('question'),
                explain=q.values()[0].get('explain'),
                types=q.values()[0].get('types'), answer=q.values()[0].get('answer'),
                option_A=q.values()[0].get('option_A'),
                option_B=q.values()[0].get('option_B'),
                option_C=q.values()[0].get('option_C'),
                option_D=q.values()[0].get('option_D'),
                option_E=q.values()[0].get('option_E'),
            )
            return JsonResponse(
                {"result": True, "message": "更新成功", "code": 201, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {"result": False, "message": "更新失败", "code": 412, "data": []},
                json_dumps_params={"ensure_ascii": False},
            )
    else:
        return JsonResponse({
            'result': False,
            'code': 405,
            'message': '请求方法错误',
            'data': {}
        })


def save_answer(request):
    """
    功能: 保存学生的答案
    输入: 题目与卷子关联id与学生的答案
    返回: 保存成功或失败
    """

    if request.method == 'POST':
        body = json.loads(request.body)
        if request.user.identity != Member.Identity.STUDENT:
            return JsonResponse({'result': False, 'code': 400, 'message': '权限错误', 'data': {}})
        student_id = request.user.id
        answer_info = body.get('answer_info')
        if not answer_info:
            return JsonResponse({'result': False, 'code': 400, 'message': '请求参数不完整', 'data': {}})

        # 将数据存入数据库
        create_list = []
        try:
            # 保证可以多次修改题目答案
            StudentAnswer.objects.filter(student_id=student_id, PQContact_id__in=list(answer_info.keys())).delete()
            for pq_id, answer in answer_info.items():
                create_list.append(StudentAnswer(
                    student_id=student_id,
                    PQContact_id=pq_id,
                    answer=answer,
                    score=0
                ))
            StudentAnswer.objects.bulk_create(create_list)
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'code': 500,
                'message': '提交失败',
                'data': {}
            })

        # 起一个celery任务去判断客观题的正误
        judge_objective.delay(list(answer_info.keys()), student_id)
        return JsonResponse({
            'result': True,
            'code': 200,
            'message': '提交成功',
            'data': {}
        })
    else:
        return JsonResponse({
            'result': False,
            'code': 405,
            'message': '请求方法错误',
            'data': {}
        })


# 老师手动批阅卷子，保存学生的分数
def teacher_correct_paper(request):
    if request.method == "POST":
        req = json.loads(request.body)  # 需要传StudentAnswer表的id和学生的分数
        student_score_list = req.get("student_answer_list")
        update_score_list = []
        for student_score in student_score_list:
            update_score_list.append(StudentAnswer(**student_score))
        try:
            StudentAnswer.objects.bulk_update(update_score_list, ["score"])  # 批量保存分数
            return JsonResponse(
                {"result": True, "message": "卷子批改成功", "code": 200, "data": []}
            )
        except DatabaseError as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "result": False,
                    "message": "卷子批改失败",
                    "code": 412,
                    "data": [],
                }
            )
    else:
        return JsonResponse(
            {
                "result": False,
                "message": "请求方法错误",
                "code": 400,
                "data": [],
            }
        )
