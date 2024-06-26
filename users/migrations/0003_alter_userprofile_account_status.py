# Generated by Django 4.2.7 on 2024-06-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_subscription_activation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_status',
            field=models.CharField(choices=[('active_trial', 'ACTIVE TRIAL'), ('expired_trial', 'EXPIRED TRIAL'), ('active_subscription', 'ACTIVE SUBSCRIPTION'), ('cancelled_subscription', 'CANCELLED SUBSCRIPTION')], default='active_trial', max_length=50),
        ),
    ]