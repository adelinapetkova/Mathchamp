from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from mathchamp.accounts.models import Student, Teacher
from mathchamp.web.models import Results

UserModel = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'grade',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        if self.instance.grade:
            profile = Student.objects.create(email=self.instance.email, user=self.instance, grade=self.instance.grade)
            profile.save()
        else:
            profile = Student.objects.create(email=self.instance.email, user=self.instance, grade=1)
            user.grade=1
            user.save()
            profile.save()
        result = Results.objects.create(user=profile, grade=profile.grade)
        result.save()
        return user


class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        profile = Teacher.objects.create(email=self.instance.email, user=self.instance)
        profile.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text=""
