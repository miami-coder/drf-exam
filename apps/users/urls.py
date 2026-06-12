from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LogoutView, ManagerCreateView, MeView, RegisterView, UpgradeToPremiumView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),

    path('login/', TokenObtainPairView.as_view(), name='auth-login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('me/', MeView.as_view(), name='auth-me'),
    path('create-manager/', ManagerCreateView.as_view(), name='auth-create-manager'),

    path('users/<int:pk>/premium/', UpgradeToPremiumView.as_view(), name='auth-upgrade-premium'),

    path('logout/', LogoutView.as_view(), name='auth-logout'),
]
