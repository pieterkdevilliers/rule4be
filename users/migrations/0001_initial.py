# Generated by Django 4.2.7 on 2024-06-25 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_up_date', models.DateField(auto_now_add=True)),
                ('trial_end_date', models.DateField()),
                ('account_status', models.CharField(choices=[('active_trial', 'ACTIVE TRIAL'), ('expired_trial', 'EXPIRED TRIAL'), ('active_subscription', 'ACTIVE SUBSCRIPTION'), ('cancelled_subscription', 'CANCELLED SUBSCRIPTION')], default='getting_started', max_length=50)),
                ('subscription_activation_date', models.DateField()),
                ('subscription_cancellation_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
