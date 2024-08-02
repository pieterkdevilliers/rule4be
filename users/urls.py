from django.urls import path
from . import views as password_reset_views

urlpatterns = [

    #     ##############################
    #     # Password Reset #
    #     ##############################

    path('password-reset/', password_reset_views.CustomPasswordResetView.as_view(
        template_name='users/password_reset_form.html',),
        name='password_reset'),
    path('password-reset/done/', password_reset_views.CustomPasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_views.CustomPasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/', password_reset_views.CustomPasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),

]
