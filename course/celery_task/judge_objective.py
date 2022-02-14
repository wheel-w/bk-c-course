from celery.task import task
import logging

from MySQLdb import DatabaseError
from course.models import StudentAnswer, PaperQuestionContact, Question

logger = logging.getLogger("root")


@task()
def judge_objective(PQContact_ids, student_id):
    try:
        PQContact_ids = [int(i) for i in PQContact_ids]
        student_answer = StudentAnswer.objects.filter(PQContact_id__in=PQContact_ids, student_id=student_id)
        answer = {pq.id: (pq.answer, pq.score, pq.types) for pq in
                  PaperQuestionContact.objects.filter(id__in=PQContact_ids)}
        for question in student_answer:
            if answer[question.PQContact_id][2] != Question.Types.SHORT_ANSWER:
                question.score = answer[question.PQContact_id][1] if question.answer == answer[question.PQContact_id][
                    0] else 0
        StudentAnswer.objects.bulk_update(student_answer, ['score'])
    except DatabaseError as e:
        logger.exception(e)
