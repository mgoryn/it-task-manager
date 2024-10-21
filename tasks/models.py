from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    team_members = models.ManyToManyField(Worker, related_name="projects")

    def __str__(self):
        return self.name


class Task(models.Model):
    priority_choices = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=priority_choices)
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    tags = models.ManyToManyField("Tag", related_name="tasks", blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
