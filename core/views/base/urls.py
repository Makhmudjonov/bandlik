from django.urls import path
from .get.student import *
from ..filters.student_filter import *

urlpatterns = [
    path("list/", StudentListView.as_view(), name="student-list"),
]