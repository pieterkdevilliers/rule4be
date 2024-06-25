from django.db import models
from django.contrib.auth.models import User
# Create your models here.

ACCOUNT_STATUS = (
    ('active_trial', 'ACTIVE TRIAL'),
    ('expired_trial', 'EXPIRED TRIAL'),
    ('active_subscription', 'ACTIVE SUBSCRIPTION'),
    ('cancelled_subscription', 'CANCELLED SUBSCRIPTION'),
)


class UserProfile(models.Model):
    '''
    Model for a user profile
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sign_up_date = models.DateField(auto_now_add=True)
    trial_end_date = models.DateField()
    account_status = models.CharField(
        max_length=50, choices=ACCOUNT_STATUS, default='getting_started')
    subscription_activation_date = models.DateField()
    subscription_cancellation_date = models.DateField()

    def __str__(self):
        return str(self.user)
