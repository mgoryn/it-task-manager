from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Position, Project, Tag, Task, TaskType, Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    filter_horizontal = ("team",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "is_complete", "priority")
    search_fields = ("name", "description")
    list_filter = ("priority", "is_complete", "project")
    filter_horizontal = ("assignees", "tags")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
