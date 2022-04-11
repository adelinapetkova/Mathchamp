from django.db import models
from django.core.validators import MinLengthValidator

from mathchamp.accounts.models import Student

POINTS_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

GRADE_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
)


class MathProblem(models.Model):
    NAME_MAX_LEN = 20
    NAME_MIN_LEN = 2
    RIGHT_ANSWER_MAX_LEN = 40

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=(
            MinLengthValidator(NAME_MIN_LEN),
        )
    )

    description = models.TextField()

    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
    )

    points = models.IntegerField(
        choices=POINTS_CHOICES,
    )

    right_answer = models.CharField(
        max_length=RIGHT_ANSWER_MAX_LEN,
    )

    solved_by = models.ManyToManyField(
        Student,
        related_name='mathproblems',
    )


class ProblemStatistics(models.Model):
    problem = models.OneToOneField(
        MathProblem,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    times_solved = models.IntegerField(
        default=0,
    )

    times_solved_right = models.IntegerField(
        default=0,
    )


class Results(models.Model):
    user = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    grade = models.IntegerField()

    points = models.IntegerField(
        default=0,
    )

    count_of_solved_problems = models.IntegerField(
        default=0,
    )
