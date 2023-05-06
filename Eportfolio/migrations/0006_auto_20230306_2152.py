# Generated by Django 3.2.5 on 2023-03-06 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eportfolio', '0005_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskType', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_Type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TypeofTask', to='Eportfolio.tasktype'),
        ),
    ]
