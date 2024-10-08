from django.contrib import admin
from tasks.models import Task, Position, TaskType, Worker


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email", "password", "first_name", "last_name", "position"
    )
    search_fields = (
        "username", "email", "first_name", "last_name", "position"
    )
    list_filter = ("position",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name", "deadline", "is_completed", "priority", "task_type"
    )
    list_filter = (
        "priority", "is_completed", "task_type"
    )
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
