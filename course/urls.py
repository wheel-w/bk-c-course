from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^update_user_info/$", views.update_user_info, name="update_user_info"),
    url(r"^manage_course/$", views.manage_course),
    url(r"^find_courses/$", views.search_courses_by_userid),
    url(r"^search_member_info/$", views.search_member_info),    # 搜寻对应身份的用户信息
    url(r"import_student_excel/", views.import_student_excel),  # 导入学生
    url(r"add_course_student/", views.add_course_student),  # 添加一个或者多个学生
    url(r"download_student_excel_template/", views.download_student_excel_template),
    url(r"search_course_student/", views.search_course_student),  # 寻找课程学生列表
    url(r"delete_student_course_contact/", views.delete_student_course_contact),  # 删除一个学生与课程对应关系
    url(r"^get_course_list/$", views.get_course_list),  # 返回课程名称的下拉列表
]
