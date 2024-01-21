from . import page_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('snapshots/', include('snapshots.urls')),
    path('api/v1/', include('snapshots.urls')),
    path('login/', page_views.load_login_page, name='load_login_page'),
]
