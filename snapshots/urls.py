from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [

    path('api/v1/aols', views.area_of_life_list, name='area_of_life_list'),
    path('api/v1/snapshots', views.snapshot_list, name='snapshot_list'),
    path('api/v1/today/<int:pk>', views.today_snapshot_list, name='today_snapshot_list'),


    path('api/v1/aols/<int:pk>', views.area_of_life_detail, name='area_of_life_detail'),
    path('api/v1/snapshots/<int:pk>', views.snapshot_detail, name='snapshot_detail'),

    path('api/v1/register/', user_views.registration_view, name='registration'),
    path('api/v1/login/', user_views.login_view, name='login'),
    path('api/v1/logout/', user_views.logout_view, name='logout'),
    

]