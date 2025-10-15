from django.urls import path
from core.views.stats.stats import StudentStatsAPIView

urlpatterns = [
    path("students/", StudentStatsAPIView.as_view(), name="student-stats"),
]
