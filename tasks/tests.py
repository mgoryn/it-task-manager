from django.test import TestCase

from .forms import TaskSearchForm, WorkerSearchForm, TeamForm, TaskForm, WorkerForm, ProjectForm
from .models import Position, Worker, Team, Project, Task, Tag, TaskType
from django.contrib.auth import get_user_model


class PositionModelTest(TestCase):
    def test_position_creation(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(position.name, "Developer")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser", password="testpassword", position=self.position
        )

    def test_worker_creation(self):
        self.assertEqual(self.worker.username, "testuser")
        self.assertEqual(self.worker.position.name, "Developer")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "testuser")


class TeamModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser", password="testpassword", position=self.position
        )
        self.team = Team.objects.create(name="Development Team", description="Team of developers")
        self.team.members.add(self.worker)

    def test_team_creation(self):
        self.assertEqual(self.team.name, "Development Team")
        self.assertEqual(self.team.members.count(), 1)
        self.assertEqual(self.team.members.first(), self.worker)

    def test_team_str(self):
        self.assertEqual(str(self.team), "Development Team")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.worker = Worker.objects.create_user(
            username="testuser", password="testpassword", position=self.position
        )
        self.team = Team.objects.create(name="Development Team", description="Team of developers")
        self.team.members.add(self.worker)
        self.project = Project.objects.create(name="New Project", description="Project description")
        self.project.team.add(self.team)

    def test_project_creation(self):
        self.assertEqual(self.project.name, "New Project")
        self.assertEqual(self.project.team.count(), 1)
        self.assertEqual(self.project.team.first(), self.team)

    def test_project_str(self):
        self.assertEqual(str(self.project), "New Project")


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Urgent")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Urgent")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Urgent")


class TaskTypeModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_type_creation(self):
        self.assertEqual(self.task_type.name, "Bug")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug")


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser", password="testpassword", position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.project = Project.objects.create(name="New Project", description="Project description")
        self.tag = Tag.objects.create(name="Urgent")
        self.task = Task.objects.create(
            name="Fix Bug",
            description="Fix the critical bug",
            deadline="2024-12-31",
            priority="High",
            task_type=self.task_type,
            project=self.project
        )
        self.task.assignees.add(self.worker)
        self.task.tags.add(self.tag)

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Fix Bug")
        self.assertEqual(self.task.description, "Fix the critical bug")
        self.assertEqual(self.task.deadline, "2024-12-31")
        self.assertEqual(self.task.priority, "High")
        self.assertEqual(self.task.task_type.name, "Bug")
        self.assertEqual(self.task.project.name, "New Project")
        self.assertEqual(self.task.assignees.count(), 1)
        self.assertEqual(self.task.assignees.first(), self.worker)
        self.assertEqual(self.task.tags.count(), 1)
        self.assertEqual(self.task.tags.first(), self.tag)

    def test_task_str(self):
        self.assertEqual(str(self.task), "Fix Bug")


# test form


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            email="testuser@example.com"
        )
        self.position = Position.objects.create(name="Developer")
        self.project = Project.objects.create(name="Test Project", description="Test Description")

    def test_project_form_valid(self):
        form_data = {"name": "New Project", "description": "A valid project description", "team": self.project.team}
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_project_form_invalid_name(self):
        form_data = {"name": "No", "description": "A valid project description", "team": self.project.team}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["Project name must me at least 3 characters long."])

    def test_worker_form_valid(self):
        form_data = {
            "username": "testworker",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "email": "worker@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.id,
        }
        form = WorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_form_duplicate_email(self):
        Worker.objects.create_user(
            username="existingworker",
            password="password123",
            email="worker@example.com",
            position=self.position
        )

        form_data = {
            "username": "newworker",
            "password1": "password123",
            "password2": "password123",
            "email": "worker@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "position": self.position.id,
        }
        form = WorkerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This email is already in use"])

    def test_task_form_valid(self):
        form_data = {
            "name": "Test Task",
            "description": "A valid task description",
            "deadline": "2024-12-31",
            "priority": "High",
            "task_type": self.project,
            "project": self.project.id,
            "assignees": [self.user.id],
            "tags": [1],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_deadline(self):
        form_data = {
            "name": "Test Task",
            "description": "A valid task description",
            "deadline": "2022-12-31",
            "priority": "High",
            "task_type": self.project,
            "project": self.project.id,
            "assignees": [self.user.id],
            "tags": [1],
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["deadline"], ["Deadline cannot be in the past."])

    def test_team_form_valid(self):
        form_data = {
            "name": "New Team",
            "description": "A valid team description",
            "members": [self.user.id]
        }
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_search_form_valid(self):
        form_data = {"name": "Test Task"}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_search_form_invalid(self):
        form_data = {"name": ""}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_search_form_valid(self):
        form_data = {"username": "testworker"}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
