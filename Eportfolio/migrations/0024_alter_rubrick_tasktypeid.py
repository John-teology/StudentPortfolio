# Generated by Django 4.0 on 2023-06-03 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eportfolio', '0023_remove_rubrick_subjectid_rubrick_gpobjt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubrick',
            name='taskTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typeRubicks', to='Eportfolio.tasktype'),
        ),
    ]
