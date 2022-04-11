from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mathchamp.accounts.models import CustomUser, Student, Teacher
from mathchamp.web.models import MathProblem

UserModel = get_user_model()


class HomeViewTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'is_student': True,
    }

    VALID_TASK_DATA = {
        'name': 'test task',
        'description': 'some text',
        'points': 3,
        'grade': 12,
        'right_answer': '45',
    }

    def __create_student_user(self):
        user = UserModel.objects.create_user(**self.VALID_STUDENT_USER_CREDENTIALS)
        profile = Student.objects.create(user=user)

        return (user, profile)

    def __create_teacher_user(self):
        user = UserModel.objects.create_user(**self.VALID_TEACHER_USER_CREDENTIALS)
        profile = Teacher.objects.create(user=user)

        return (user, profile)

    def __create_task(self):
        task = MathProblem.objects.create(**self.VALID_TASK_DATA)
        task.save()

        return task

    def __get_response(self):
        return self.client.get(reverse('index'))

    def test_when_valid_user_data__expect_correct_home_page_template(self):
        user, profile = self.__create_student_user()
        self.__get_response()
        self.assertTemplateUsed('web/home.html')

    def test_when_valid_user_data__expect_correct_user_in_context(self):
        user, profile = self.__create_teacher_user()
        self.client.login(**self.VALID_TEACHER_USER_CREDENTIALS)
        response = self.__get_response()

        self.assertEqual(user, response.context['user'])

    def test_when_valid_user_data_and_valid_tasks__expect_correct_tasks_list_in_context(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)
        task = self.__create_task()
        response = self.__get_response()

        self.assertListEqual([task], list(response.context['tasks']))

    def test_when_valid_student_data_and_valid_tasks__expect_empty_solved_tasks_list_in_context(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)
        task = self.__create_task()
        response = self.__get_response()

        self.assertListEqual([], list(response.context['solved_tasks_by_student']))
