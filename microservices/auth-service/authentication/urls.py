from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView, health

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("health/", health, name="health")
]