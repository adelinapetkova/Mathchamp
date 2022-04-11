from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mathchamp.accounts.models import Student, Teacher
from mathchamp.web.forms import SubmitAnswerForm
from mathchamp.web.models import MathProblem, Results, ProblemStatistics

UserModel = get_user_model()


class ProfileDetailsTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'grade': 11,
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

    def __get_response(self):
        return self.client.get(reverse('profile details'))

    def test_when_valid_student_data__expect_correct_template(self):
        user, profile = self.__create_student_user()
        self.__get_response()
        self.assertTemplateUsed('web/profile-details.html')

    def test_when_valid_teacher_data__expect_correct_user_in_context(self):
        user, profile = self.__create_teacher_user()
        self.client.login(**self.VALID_TEACHER_USER_CREDENTIALS)
        response = self.__get_response()

        expected_context = {
            'user': user,
        }

        self.assertEqual(expected_context['user'], response.context['user'])

    def test_when_valid_student_data__expect_correct_context(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)
        result = Results.objects.create(user=profile, grade=user.grade)
        response = self.__get_response()

        expected_context = {
            'profile': profile,
            'user': user,
            'result': result,
        }

        actual_context = {
            'profile': response.context['profile'],
            'user': response.context['user'],
            'result': response.context['result'],
        }

        self.assertDictEqual(expected_context, actual_context)


class EditProfileTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'grade': 11,
        'is_student': True,
    }

    def __create_student_user(self):
        user = UserModel.objects.create_user(**self.VALID_STUDENT_USER_CREDENTIALS)
        profile = Student.objects.create(user=user)

        return (user, profile)

    def __create_teacher_user(self):
        user = UserModel.objects.create_user(**self.VALID_TEACHER_USER_CREDENTIALS)
        profile = Teacher.objects.create(user=user)

        return (user, profile)

    def __get_response(self):
        return self.client.get(reverse('edit profile'))

    def test_when_valid_teacher_data__expect_correct_template(self):
        user, profile = self.__create_teacher_user()
        self.__get_response()
        self.assertTemplateUsed('web/edit-profile.html')

    def test_when_valid_student_data__expect_correct_user_and_profile(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)
        response = self.__get_response()

        expected_context = {
            'profile': profile,
            'user': user,
        }

        actual_context = {
            'profile': response.context['profile'],
            'user': response.context['user'],
        }

        self.assertDictEqual(expected_context, actual_context)

    def test_when_valid_teacher_data__expect_correct_user_and_profile(self):
        user, profile = self.__create_teacher_user()
        self.client.login(**self.VALID_TEACHER_USER_CREDENTIALS)
        response = self.__get_response()

        expected_context = {
            'profile': profile,
            'user': user,
        }

        actual_context = {
            'profile': response.context['profile'],
            'user': response.context['user'],
        }

        self.assertDictEqual(expected_context, actual_context)


class DeleteProfileTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'grade': 11,
        'is_student': True,
    }

    def __create_student_user(self):
        user = UserModel.objects.create_user(**self.VALID_STUDENT_USER_CREDENTIALS)
        profile = Student.objects.create(user=user)

        return (user, profile)

    def __create_teacher_user(self):
        user = UserModel.objects.create_user(**self.VALID_TEACHER_USER_CREDENTIALS)
        profile = Teacher.objects.create(user=user)

        return (user, profile)

    def __get_response(self, profile):
        return self.client.get(reverse('delete profile', kwargs={'pk': profile.pk}))

    def test_when_valid_teacher_data__expect_correct_template(self):
        user, profile = self.__create_teacher_user()
        self.__get_response(profile)
        self.assertTemplateUsed('web/delete-profile.html')

    def test_when_valid_student_data__expect_correct_user_and_profile(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)
        response = self.__get_response(profile)

        expected_context = {
            'user': user,
        }

        actual_context = {
            'user': response.context['user'],
        }

        self.assertDictEqual(expected_context, actual_context)


class ResultsTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'grade': 11,
        'is_student': True,
    }

    def __create_student_user(self):
        user = UserModel.objects.create_user(**self.VALID_STUDENT_USER_CREDENTIALS)
        profile = Student.objects.create(user=user)

        return (user, profile)

    def __create_teacher_user(self):
        user = UserModel.objects.create_user(**self.VALID_TEACHER_USER_CREDENTIALS)
        profile = Teacher.objects.create(user=user)

        return (user, profile)

    def __get_response(self):
        return self.client.get(reverse('results'))

    def test_when_valid_teacher_data__expect_correct_template(self):
        user, profile = self.__create_teacher_user()
        self.__get_response()
        self.assertTemplateUsed('web/results.html')

    def test_when_valid_student_data__expect_correct_user_and_results(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)
        result = Results.objects.create(user_id=user.pk, grade=user.grade)
        response = self.__get_response()

        expected_context = {
            'results': [result],
            'user': user,
        }

        actual_context = {
            'results': list(response.context['results']),
            'user': response.context['user'],
        }

        self.assertDictEqual(expected_context, actual_context)


class SubmitAnswerTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'grade': 11,
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

    def __get_response(self, task):
        return self.client.get(reverse('solve task', kwargs={'pk': task.pk}))

    def test_when_valid_student_data__expect_correct_template(self):
        user, profile = self.__create_student_user()
        task = MathProblem.objects.create(**self.VALID_TASK_DATA)
        self.__get_response(task)
        self.assertTemplateUsed('web/solve-task.html')

    def test_when_valid_student_data__expect_correct_form_and_task_in_context(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)

        task = MathProblem.objects.create(**self.VALID_TASK_DATA)
        ProblemStatistics.objects.create(problem_id=task.pk)
        Results.objects.create(user_id=user.pk, grade=user.grade)
        form = SubmitAnswerForm()

        response = self.__get_response(task)

        expected_context = {
            'task': task,
        }

        actual_context = {
            'task': response.context['task'],
        }

        self.assertDictEqual(expected_context, actual_context)


class TaskDetailsTests(TestCase):
    VALID_TEACHER_USER_CREDENTIALS = {
        'email': 'testteacher@abv.bg',
        'password': 'theteacher',
        'is_teacher': True,
    }

    VALID_STUDENT_USER_CREDENTIALS = {
        'email': 'teststudent@abv.bg',
        'password': 'thestudent',
        'grade': 11,
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

    def __get_response(self, task):
        return self.client.get(reverse('task details', kwargs={'pk': task.pk}))

    def test_when_valid_student_data__expect_correct_template(self):
        user, profile = self.__create_student_user()
        self.client.login(**self.VALID_STUDENT_USER_CREDENTIALS)

        task = MathProblem.objects.create(**self.VALID_TASK_DATA)

        ProblemStatistics.objects.create(problem_id=task.pk)
        self.__get_response(task)

        self.assertTemplateUsed('web/task-details.html')
