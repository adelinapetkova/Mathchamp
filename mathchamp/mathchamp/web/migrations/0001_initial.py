# Generated by Django 4.0.3 on 2022-03-25 15:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_alter_customuser_managers_student_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MathProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(2)])),
                ('description', models.TextField()),
                ('grade', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=2)),
                ('points', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('right_answer', models.CharField(max_length=40)),
                ('solved_by', models.ManyToManyField(to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemStatistics',
            fields=[
                ('problem_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='web.mathproblem')),
            ],
        ),
    ]
