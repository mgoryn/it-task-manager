from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from tasks.models import Position, Project, Tag, Task, Team, Worker


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "team"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise ValidationError("Project name must me at least 3 characters long.")
        return name


class WorkerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=True)

    class Meta:
        model = Worker
        fields = ["username",
                  "password1",
                  "password2",
                  "email",
                  "first_name",
                  "last_name",
                  "position",
                  ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Worker.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise ValidationError("Position name must me at least 3 characters long.")
        return name


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task name"
            }
        )
    )


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by team name"
            }
        )
    )


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by tag name"
            }
        )
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by worker username"
            }
        )
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by project name"
            }
        )
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "project",
            "assignees",
            "tags"
        ]
        widgets = {
            "deadline": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "YYYY-MM-DD"
            }),
            "assignees": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-input"
            }),
            "tags": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < datetime.date.today():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description", "members"]
        widgets = {
            "members": forms.CheckboxSelectMultiple,
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "placeholder": "Username",
            "class": "form-control"
        })
        self.fields["password"].widget.attrs.update({
            "placeholder": "Password",
            "class": "form-control"
        })
