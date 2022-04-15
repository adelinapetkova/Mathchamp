from django import forms
from django.contrib.auth import get_user_model

from mathchamp.accounts.models import Student, Teacher
from mathchamp.web.models import Results

UserModel = get_user_model()


class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        custom_user=UserModel.objects.get(pk=self.instance.user_id)
        result=Results.objects.get(user_id=self.instance.user_id)
        result.grade=self.instance.grade
        custom_user.grade=self.instance.grade
        result.save()
        custom_user.save()


class EditTeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ('user', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = None


class SubmitAnswerForm(forms.Form):
    ANSWER_MAX_LEN = 40

    answer = forms.CharField(
        max_length=ANSWER_MAX_LEN,
        label='Answer',
    )


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        user_id=self.instance.id

        if self.instance.is_student:
            Results.objects.get(pk=user_id).delete()
            Student.objects.get(pk=user_id).delete()
        else:
            Teacher.objects.get(pk=user_id).delete()

        self.instance.delete()

        return self.instance

    class Meta:
        model = UserModel
        fields = ()
