# Generated by Django 4.0 on 2023-06-04 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eportfolio', '0032_rename_cptype_task_tasktype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectRubrick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(null=True)),
                ('gpObjt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subGpRubrick', to='Eportfolio.gptype')),
                ('subjectObj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjectRub', to='Eportfolio.subject')),
            ],
        ),
    ]
