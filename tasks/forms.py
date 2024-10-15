from django import forms
from tasks.models import Task, Worker, Project, Team


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "worker", "task_type", "project"]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]


class TeamForm(forms.ModelForm):
    model = Team
    fields = ["name", "members"]


class WorkerSearchForm(forms.Form):
    username = forms.CharField(required=False)


class TaskSearchForm(forms.Form):
    name = forms.CharField(required=False)


class ProjectSearchForm(forms.Form):
    name = forms.CharField(required=False)


class TeamSearchForm(forms.Form):
    name = forms.CharField(required=False)
