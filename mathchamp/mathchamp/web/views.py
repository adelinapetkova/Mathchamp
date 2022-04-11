from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from mathchamp.accounts.models import Student, Teacher
from mathchamp.web.decorators import students_only, teachers_only
from mathchamp.web.forms import EditStudentProfileForm, EditTeacherProfileForm, SubmitAnswerForm, DeleteProfileForm
from mathchamp.web.models import MathProblem, ProblemStatistics, Results

UserModel = get_user_model()


class AboutUsView(generic.TemplateView):
    template_name = 'web/about-us.html'


class CreateMathProblemView(LoginRequiredMixin, CreateView):
    model = MathProblem
    template_name = 'web/add-task.html'
    fields = ('name', 'description', 'grade', 'points', 'right_answer')

    success_url = reverse_lazy('index')

    @method_decorator(teachers_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        ProblemStatistics.objects.create(problem_id=self.object.id)
        return super().form_valid(form)


class EditMathProblemView(LoginRequiredMixin, UpdateView):
    model = MathProblem
    template_name = 'web/edit-task.html'
    fields = ('name', 'description', 'grade', 'points', 'right_answer')
    success_url = reverse_lazy('index')

    @method_decorator(teachers_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def show_profile_details(request):
    student_ids = Student.objects.all().values_list('pk', flat=True)
    user = UserModel.objects.get(pk=request.user.id)

    if request.user.id in student_ids:
        profile = Student.objects.get(pk=request.user.id)
        result = Results.objects.get(pk=request.user.id)
    else:
        profile = Teacher.objects.get(pk=request.user.id)
        result = None

    context = {
        'profile': profile,
        'user': user,
        'result': result,
    }

    return render(request, 'web/profile-details.html', context)


@login_required
def edit_profile(request):
    student_ids = Student.objects.all().values_list('pk', flat=True)
    user = UserModel.objects.get(pk=request.user.id)

    if request.user.id in student_ids:
        profile = Student.objects.get(pk=request.user.id)
        edit_form = EditStudentProfileForm
    else:
        profile = Teacher.objects.get(pk=request.user.id)
        edit_form = EditTeacherProfileForm

    if request.method == 'POST':
        form = edit_form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = edit_form(instance=profile)

    context = {
        'form': form,
        'user': user,
        'profile': profile,
    }
    return render(request, 'web/edit-profile.html', context)


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'web/delete-profile.html'
    form_class = DeleteProfileForm
    success_url = reverse_lazy('unauthenticated home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user']=user
        return context


class ResultsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'web/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student:
            results = Results.objects.order_by('-points').filter(grade=user.grade)
        else:
            results = Results.objects.order_by('-points', 'grade')

        context['results'] = results
        context['user'] = user
        return context


@login_required
@students_only
def submit_answer(request, pk):
    task = MathProblem.objects.get(pk=pk)
    student = Student.objects.get(pk=request.user.id)
    problem_statistics = ProblemStatistics.objects.get(pk=task.pk)
    result = Results.objects.get(pk=student.pk)

    if request.method == 'POST':
        submit_form = SubmitAnswerForm(request.POST)

        if submit_form.is_valid():
            problem_statistics.times_solved += 1
            problem_statistics.save()
            if task.right_answer == submit_form.cleaned_data['answer']:
                task.solved_by.add(student)
                problem_statistics.times_solved_right += 1
                result.points += task.points
                result.count_of_solved_problems += 1

                result.save()
                problem_statistics.save()
                task.save()
            return redirect('index')
    else:
        submit_form = SubmitAnswerForm()

    context = {
        'submit_form': submit_form,
        'task': task,
    }
    return render(request, 'web/solve_task.html', context)


@login_required
def task_details(request, pk):
    task=MathProblem.objects.get(pk=pk)
    problem_statistics = ProblemStatistics.objects.get(pk=task.pk)
    user = UserModel.objects.get(pk=request.user.id)
    context={}
    success_rate=0

    if problem_statistics.times_solved>0:
        success_rate=(problem_statistics.times_solved_right/problem_statistics.times_solved)*100

    if user.is_student:
        student_profile = Student.objects.get(pk=user.id)
        solved_tasks = student_profile.mathproblems.all()
        context['solved_tasks_by_student'] = solved_tasks

    context['task']=task
    context['user']=user
    if not success_rate==0:
        context['success_rate']=f"{success_rate:.2f}"

    return render(request, 'web/task-details.html', context)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
