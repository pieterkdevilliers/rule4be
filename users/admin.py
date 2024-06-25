from django.contrib import admin
from users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin Interface Display Settings
    """
    list_display = ('user', 'sign_up_date', 'trial_end_date', 'account_status')
    ordering = ['sign_up_date', 'trial_end_date', 'account_status']


admin.site.register(UserProfile, UserProfileAdmin)
