# core/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views.login.login import UserLoginAPIView


urlpatterns = [
    # path("upload-json/", UploadStudentJSONView.as_view(), name="upload-jsons"),
    # path("stats/", StudentStatsAPIView.as_view(), name="student-stats"),

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("sync/", include("core.views.sync.urls")),
    path("stats/", include("core.views.stats.urls")),
    path("students/", include("core.views.base.urls")),
    path("base/", include("core.views.filters.urls"))

]
