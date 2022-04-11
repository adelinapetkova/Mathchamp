from django.urls import path

from mathchamp.accounts.views import HomeView, StudentRegistrationView, TeacherRegistrationView, UserLoginView, \
    UserLogoutView, UserPasswordChange, HomeUnauthView

urlpatterns = (
    path('student-register/', StudentRegistrationView.as_view(), name='register student'),
    path('teacher-register/', TeacherRegistrationView.as_view(), name='register teacher'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', UserPasswordChange.as_view(), name='password_change_done'),
    path('', HomeUnauthView.as_view(), name='unauthenticated home'),
)
