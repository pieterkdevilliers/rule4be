from . import page_views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('snapshots/', include('snapshots.urls')),
    path('api/v1/', include('snapshots.urls')),
    path('', page_views.load_login_page, name='load_login_page'),
    path('signup/', page_views.load_signup_page, name='signup'),
    path('logout/', page_views.logout_view, name='logout_view'),
    path('aols/', page_views.load_aols_page, name='load_aols_page'),
    path('today/<int:pk>', page_views.load_today_snapshot_page,
         name='load_today_snapshot_page'),

    path('create-aol/', page_views.create_aol, name='create_aol'),
    path('edit-aol/<int:aol_id>', page_views.edit_aol, name='edit_aol'),
    path('delete-aol/<int:aol_id>', page_views.delete_aol, name='delete_aol'),
    path('create-snapshot/<int:aol_id>',
         page_views.create_snapshot, name='create_snapshot'),

]
