# Generated by Django 4.0.3 on 2022-03-30 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_managers_student_email_and_more'),
        ('web', '0003_rename_problem_id_problemstatistics_problem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mathproblem',
            name='solved_by',
            field=models.ManyToManyField(related_name='mathproblems', to='accounts.student'),
        ),
    ]