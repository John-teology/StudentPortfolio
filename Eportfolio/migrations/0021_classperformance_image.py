# Generated by Django 4.0 on 2023-06-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eportfolio', '0020_cptype_gptype_remove_subject_units_gradeperiods_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classperformance',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
