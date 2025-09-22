# core/urls.py
from django.urls import path
from .views import LoginAPIView, StudentStatsAPIView, UploadStudentJSONView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("upload-json/", UploadStudentJSONView.as_view(), name="upload-jsons"),
    path("stats/", StudentStatsAPIView.as_view(), name="student-stats"),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", LoginAPIView.as_view(), name="login"),

]
