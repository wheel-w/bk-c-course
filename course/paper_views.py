import json
import logging

from MySQLdb import DatabaseError
from django.db import transaction
from django.http import JsonResponse

from .models import CustomType, Member, Paper, PaperQuestionContact, Question
from .views import is_teacher

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
        body = json.loads(request.body)
        course_id = body.get('course_id')
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


@is_teacher
def paper(request):
    method = request.method

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

    if method == "GET":
        """
        功能: 1. 根据老师id，返回给老师的所有卷子
             2. 根据老师id与课程id，返回对应老师教的本门课程的所有卷子
             3. 根据question_id查询所含该题目的卷子
        输入：老师id或老师与课程id
        返回：对应卷子信息
        """
        body = json.loads(request.body)
        query_param = {'teacher': str(Member.objects.get(id=request.user.id))}
        if 'course_id' in body.keys():
            query_param['course_id'] = body.get('course_id')
        try:
            if 'question_id' in body.keys():
                question_id = body.get('question_id')
                query_param['id__in'] = [pq.paper_id for pq in
                                         PaperQuestionContact.objects.filter(question_id=question_id)]

            paper_info = list(Paper.objects.filter(**query_param).values())

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

    else:
        return JsonResponse({
            'result': False,
            'code': 405,
            'message': '请求方法错误'
        })


@is_teacher
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
        body = json.loads(request.body)
        paper_id = body.get('paper_id')

        if paper_id is None:
            return JsonResponse({
                'result': False,
                'code': 400,
                'message': '请求参数不完整(没有paper_id)',
                'data': {}
            })

        try:
            order = json.loads(Paper.objects.get(id=paper_id).question_order)
            custom_type_ids = order.keys()
            questions = {pq['id']: pq for pq in PaperQuestionContact.objects.filter(paper_id=paper_id).values()}

            # 初始化传输题目的格式
            question_data = {
                'titles': {i.id: i.custom_type_name for i in CustomType.objects.filter(id__in=custom_type_ids)},
                'questions': {i: [] for i in custom_type_ids}}
        except Exception as e:
            logger.exception(e)
            return JsonResponse({
                'result': False,
                'code': 500,
                'message': '查询失败(请检查日志)',
                'date': {}
            })

        # 在题目表中获得对应id对应的大题名称 (id:name)
        # 将题目信息中的custom_type_id变为custom_type_name
        for title_id, question_ids in order.items():
            for q_id in question_ids:
                q = questions[q_id]
                q.pop('answer')
                q.pop('explain')
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

            # 删除上一次的信息，将本次的题目数据进行添加
            PaperQuestionContact.objects.filter(paper_id=paper_id).delete()
            PaperQuestionContact.objects.bulk_create(create_obj_list)

            # 构造Json数据(顺序不能变)
            for PQContact in PaperQuestionContact.objects.filter(paper_id=paper_id):
                score_list[question_id_list.index(PQContact.question_id)] = PQContact.id

            sum = 0
            order_json = {}
            for title in title_info:
                order_json[title[0]] = score_list[sum:sum+title[1]]
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
