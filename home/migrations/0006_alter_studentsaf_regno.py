# Generated by Django 4.2.17 on 2025-01-01 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_studentsaf_regno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsaf',
            name='regNo',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]
