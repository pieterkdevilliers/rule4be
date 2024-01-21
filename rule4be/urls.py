from . import page_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('snapshots/', include('snapshots.urls')),
    path('api/v1/', include('snapshots.urls')),
    path('', page_views.load_login_page, name='load_login_page'),
    path('aols/', page_views.load_aols_page, name='load_aols_page'),
    path('today/<int:pk>', page_views.load_today_snapshot_page, name='load_today_snapshot_page'),
]
