# Generated by Django 4.0.3 on 2022-03-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_results'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problemstatistics',
            old_name='problem_id',
            new_name='problem',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='problemstatistics',
            name='times_solved',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problemstatistics',
            name='times_solved_right',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='results',
            name='count_of_solved_problems',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='results',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
