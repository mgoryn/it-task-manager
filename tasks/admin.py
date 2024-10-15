from django.contrib import admin
from tasks.models import Task, Worker, TaskType, Project, Team, Position


@admin.site.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "worker", "task_type", "project", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("user", "position")
    search_fields = ("user__username",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at",)
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
