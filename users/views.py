from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class CustomPasswordResetView(auth_views.PasswordResetView):
    """
    Custom Password Reset View
    """
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    Custom Password Reset Done View
    """
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    Custom Password Reset Confirm View
    """
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """
    Custom Password Reset Complete View
    """
    template_name = 'registration/password_reset_complete.html'
