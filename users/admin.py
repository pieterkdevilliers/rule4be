from django.contrib import admin
from users.models import UserProfile, CheckoutSessionRecord


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin Interface Display Settings
    """
    list_display = ('user', 'sign_up_date', 'trial_end_date', 'account_status')
    ordering = ['sign_up_date', 'trial_end_date', 'account_status']


class CheckoutSessionRecordAdmin(admin.ModelAdmin):
    """
    Admin Interface Display Settings
    """
    list_display = ('user', 'stripe_customer_id',
                    'stripe_checkout_session_id', 'stripe_price_id')
    ordering = ['user', 'stripe_customer_id',
                'stripe_checkout_session_id', 'stripe_price_id']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CheckoutSessionRecord, CheckoutSessionRecordAdmin)
