# Generated by Django 4.2.7 on 2024-08-01 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0004_alter_snapshot_image_alter_snapshot_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapshot',
            name='body',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
