from django.contrib import admin

from mathchamp.web.models import MathProblem, ProblemStatistics, Results


@admin.register(MathProblem)
class MathProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'points',)
    ordering = ['grade', 'points',]

