# Generated by Django 4.0 on 2023-06-03 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eportfolio', '0025_gradeperiods_score_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradeperiods',
            name='student',
        ),
    ]
