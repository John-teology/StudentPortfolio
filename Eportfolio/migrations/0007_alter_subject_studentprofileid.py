# Generated by Django 3.2.5 on 2023-03-06 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eportfolio', '0006_auto_20230306_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='studentProfileID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentSubject', to='Eportfolio.studentprofile'),
        ),
    ]
