from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import UserViewSet, get_jwt_token, send_confirm_code

router_users_v1 = DefaultRouter()
router_users_v1.register(r'users', UserViewSet, basename='users')

v1_auth_patterns = [
    path('token/', get_jwt_token, name='get_token'),
    path('email/', send_confirm_code, name='send_email'),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(router_users_v1.urls)),
]
