from django.urls import path
from ..filters.student_filter import *

urlpatterns = [
    path("universities/", UniversityListView.as_view(), name="university-list"),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("specialties/", SpecialtyListView.as_view(), name="specialty-list"),
    path("levels/", LevelListView.as_view(), name="level-list"),
    path("education-forms/", EducationFormListView.as_view(), name="education-form-list"),
    path("education-types/", EducationTypeListView.as_view(), name="education-type-list"),
    path("payment-forms/", PaymentFormListView.as_view(), name="payment-form-list"),
    path("student-types/", StudentTypeListView.as_view(), name="student-type-list"),
    path("social-categories/", SocialCategoryListView.as_view(), name="social-category-list"),
    path("accommodations/", AccommodationListView.as_view(), name="accommodation-list"),
    path("citizenships/", CitizenshipListView.as_view(), name="citizenship-list"),
    path("genders/", GenderListView.as_view(), name="gender-list"),
    path("provinces/", ProvinceListView.as_view(), name="province-list"),
    path("districts/", DistrictListView.as_view(), name="district-list"),
    path("terrains/", TerrainListView.as_view(), name="terrain-list"),
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("semesters/", SemesterListView.as_view(), name="semester-list"),
    path("education-years/", EducationYearListView.as_view(), name="education-year-list"),
]