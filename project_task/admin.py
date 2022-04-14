"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版（BLUEKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. ALL rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MII
Unless required by applicable Law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific Language governing permissions and limitations under the License.
"""
from django.contrib import admin

from .models import ProjectTask, StudentProjectTaskInfo


class ProjectTaskAdmin(admin.ModelAdmin):
    list_filter = (
        "project_id",
        "id",
        "title",
        "types",
        "status",
        "created_id",
        "updated_id",
    )


class StudentProjectTaskInfoAdmin(admin.ModelAdmin):
    list_filter = (
        "project_id",
        "id",
        "project_task_id",
        "status",
        "total_score",
        "created_id",
        "updated_id",
    )


# Register your models here.
admin.site.register(ProjectTask, ProjectTaskAdmin)
admin.site.register(StudentProjectTaskInfo, StudentProjectTaskInfoAdmin)
