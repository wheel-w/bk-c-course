from django.shortcuts import render

from course import models

# Create your views here.


# 增
def course_add(request):
    if request.method == "POST":
        courseName = request.POST.get("courseName", "")
        courseIntroduction = request.POST.get("courseIntroduction", "")
        teacher = request.POST.get("teacher", "")
        createPeople = request.POST.get("createPeople", "")
        manageStudent = request.POST.get("manageStudent", "")  # 接收前端传递的数据
        models.Course.objects.create(
            course_name=courseName,
            course_introduction=courseIntroduction,
            teacher=teacher,
            create_people=createPeople,
            manage_student=manageStudent,
        )  # 将得到的数据加到course表
    courseInfo = models.Course.objects.all()  # 获取course表的所有数据
    return render(request, "", {"courseInfo": courseInfo})


# 删
def course_delete(request):
    if request.method == "DELETE":
        courseId = request.DELETE.get("courseId", "")  # 接收前端传递的数据
        models.Course.objects.filter(id=courseId).delete()  # 删除course表中对应信息
    courseInfo = models.Course.objects.all()  # 获取course表中的数据
    return render(request, "", {"courseInfo": courseInfo})


# 查
def course_find(request):
    courseName = []
    if request.method == "POST":
        userId = request.POST.get("userId", "1")  # 1
        find_courses_ids = models.UserCourseContact.objects.filter(
            user_id=userId
        ).values("course_name")
        for find_courses_id in find_courses_ids:
            find_course_name = models.Course.objects.filter(
                course_id=find_courses_id
            ).values("course_name")
            courseName.append(find_course_name)
    return render(request, "", {"courseName", courseName})


# 改
def course_alter(request):
    new_course = []
    if request.method == "POST":
        courseId = request.POST.get("courseId", "1")  # 1
        courseName = request.POST.get("courseName", "")  # '课程名称'
        courseIntroduction = request.POST.get("courseIntroduction", "")  # '课程简介'
        teacher = request.POST.get("teacher", "")  # '教师姓名'
        createPeople = request.POST.get("createPeople", "")  # '创建人'
        manageStudent = request.POST.get("manageStudent", "")  # '学生管理员'
        models.Course.objects.filter(id=courseId).update(
            course_name=courseName,
            course_introduction=courseIntroduction,
            teacher=teacher,
            create_people=createPeople,
            manage_student=manageStudent,
        )
        new_course = models.Course.objects.filter(id=courseId)
    return render(request, "", {"course": new_course})