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
    trial_end_date = models.DateField(null=True, blank=True)
    account_status = models.CharField(
        max_length=50, choices=ACCOUNT_STATUS, default='active_trial')
    subscription_activation_date = models.DateField(null=True, blank=True)
    subscription_cancellation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class CheckoutSessionRecord(models.Model):
    """
    Model to store the checkout session details
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user who initiated the checkout."
    )
    stripe_customer_id = models.CharField(max_length=255)
    stripe_checkout_session_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    has_access = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
