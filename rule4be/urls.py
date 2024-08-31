from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import page_views, stripe_views

urlpatterns = [
     path("admin/", admin.site.urls),
     path('accounts/', include('django.contrib.auth.urls')),
     path('api-auth/', include('rest_framework.urls')),
     path('snapshots/', include('snapshots.urls')),
     path('users/', include('users.urls')),
     path('api/v1/', include('snapshots.urls')),
     path('', page_views.load_login_page, name='load_login_page'),
     path('login-signup-section', page_views.load_login_signup_section, name='load_login_signup_section'),
     path('login-form', page_views.load_login_form, name='load_login_form'),
     path('signup/', page_views.load_signup_page, name='signup'),
     path('logout/', page_views.logout_view, name='logout_view'),
     path('aols/', page_views.load_aols_page, name='load_aols_page'),
     path('today/<int:pk>', page_views.load_today_snapshot_page,
          name='load_today_snapshot_page'),
     path('load-user-profile', page_views.load_user_profile,
          name='load_user_profile'),
     path('load-trial-expired-page', page_views.load_trial_expired_page,
          name='load_trial_expired_page'),

     path('create-aol/', page_views.create_aol, name='create_aol'),
     path('edit-aol/<int:aol_id>', page_views.edit_aol, name='edit_aol'),
     path('delete-aol/<int:aol_id>', page_views.delete_aol, name='delete_aol'),
     path('create-snapshot/<int:aol_id>',
          page_views.create_snapshot, name='create_snapshot'),

     ##############################
     # Stripe Payment Integration #
     ##############################

     path('subscribe/', stripe_views.subscribe, name='subscribe'),
     path('cancel/', stripe_views.cancel, name='cancel'),
     path('success/', stripe_views.success, name='success'),
     path('create-checkout-session/', stripe_views.create_checkout_session,
          name='create-checkout-session'),
     path('direct-to-customer-portal/', stripe_views.direct_to_customer_portal,
          name='direct-to-customer-portal'),
     path('collect-stripe-webhook/', stripe_views.collect_stripe_webhook,
          name='collect-stripe-webhook'),

     path('privacy-policy/', page_views.privacy_policy,
          name='privacy_policy'),
     path('terms-and-conditions/', page_views.terms_and_conditions,
          name='terms_and_conditions'),

     ]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)
