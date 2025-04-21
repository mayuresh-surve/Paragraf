from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView, health
from .views import UserDetailView, UserSearchView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/<uuid:id>/", UserDetailView.as_view(), name="user_detail"),
    path("users/", UserSearchView.as_view(), name="find_user_by_email"),
    path("health/", health, name="health"),
]