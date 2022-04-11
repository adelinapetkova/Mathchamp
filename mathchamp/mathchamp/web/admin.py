from django.contrib import admin

from mathchamp.web.models import MathProblem, ProblemStatistics, Results


@admin.register(MathProblem)
class MathProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(ProblemStatistics)
class ProblemStatisticsAdmin(admin.ModelAdmin):
    pass


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    pass
