# Generated by Django 4.0.3 on 2022-03-25 13:37

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import mathchamp.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_student_teacher'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[mathchamp.accounts.models.characters_validator, django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[mathchamp.accounts.models.characters_validator, django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[mathchamp.accounts.models.characters_validator, django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[mathchamp.accounts.models.characters_validator, django.core.validators.MinLengthValidator(2)]),
        ),
    ]