from django.urls import path
from api.views import views_fbv

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = "api"

urlpatterns = [
    path('sign-up/', views_fbv.sign_up_user, name="user_create"),
    path("check/", views_fbv.check, name="check"),

    path('sign-in/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify")
]