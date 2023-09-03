from django.urls import path
from . import views
from users import views as user_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/aols', views.area_of_life_list, name='area_of_life_list'),
    path('api/v1/snapshots', views.snapshot_list, name='snapshot_list'),
    path('api/v1/today/<int:pk>', views.today_snapshot_list, name='today_snapshot_list'),


    path('api/v1/aols/<int:pk>', views.area_of_life_detail, name='area_of_life_detail'),
    path('api/v1/snapshots/<int:pk>', views.snapshot_detail, name='snapshot_detail'),

    path('api/v1/user-register/', user_views.user_register, name='user_register'),
    

]