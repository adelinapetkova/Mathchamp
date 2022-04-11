from django.contrib import admin

from mathchamp.accounts.models import CustomUser, Student, Teacher


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_student', 'is_teacher', 'is_superuser',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'grade',)
    ordering = ['grade',]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('email',)



