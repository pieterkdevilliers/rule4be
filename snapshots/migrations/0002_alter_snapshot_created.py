# Generated by Django 4.1.3 on 2023-08-25 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("snapshots", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snapshot",
            name="created",
            field=models.DateField(auto_now_add=True),
        ),
    ]
