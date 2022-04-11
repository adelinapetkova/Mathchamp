from django.urls import path

from mathchamp.accounts.views import HomeView
from mathchamp.web.views import CreateMathProblemView, EditMathProblemView, show_profile_details, ResultsView, \
    edit_profile, submit_answer, DeleteProfileView, AboutUsView, task_details

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('about-us/', AboutUsView.as_view(), name='about us'),

    path('add-task/', CreateMathProblemView.as_view(), name='add task'),
    path('edit-task/<int:pk>/', EditMathProblemView.as_view(), name='edit task'),
    path('solve-task/<int:pk>/', submit_answer, name='solve task'),
    path('task-details/<int:pk>/', task_details, name='task details'),

    path('profile-details/', show_profile_details, name='profile details'),
    path('profile-edit/', edit_profile, name='edit profile'),
    path('profile-delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),

    path('results/', ResultsView.as_view(), name='results'),
)

