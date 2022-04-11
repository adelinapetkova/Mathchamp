from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from mathchamp.accounts.forms import StudentRegistrationForm, TeacherRegistrationForm, CustomPasswordChangeForm
from mathchamp.accounts.models import Teacher, Student
from mathchamp.web.models import MathProblem, Results

UserModel = get_user_model()


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        math_problems = MathProblem.objects.order_by('grade', 'points')
        user = self.request.user

        if isinstance(user, UserModel):
            if user.is_student:
                student_profile = Student.objects.get(pk=user.id)
                solved_tasks = student_profile.mathproblems.all()
                context['solved_tasks_by_student'] = solved_tasks

        context['tasks'] = math_problems
        context['user'] = user
        return context


class HomeUnauthView(generic.TemplateView):
    template_name = 'web/home-unauth.html'


class StudentRegistrationView(generic.CreateView):
    form_class = StudentRegistrationForm
    template_name = 'accounts/register_student.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super(StudentRegistrationView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid


class TeacherRegistrationView(generic.CreateView):
    form_class = TeacherRegistrationForm
    template_name = 'accounts/register_teacher.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super(TeacherRegistrationView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('index')


class UserLogoutView(LogoutView):
    pass


class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = '/web/'
    form_class = CustomPasswordChangeForm
