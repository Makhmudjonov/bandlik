from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.modellar.student import *
from core.serializers.student_serializer import *

# 🔹 Umumiy ListAPIView generator
class BaseListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Nom bo‘yicha qidirish",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        """Filter uchun ro‘yxat"""
        return super().get(request, *args, **kwargs)

class UniversityListView(BaseListAPIView):
    queryset = University.objects.all().order_by("name")
    serializer_class = UniversitySerializer

class DepartmentListView(BaseListAPIView):
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentSerializer

class SpecialtyListView(BaseListAPIView):
    queryset = Specialty.objects.all().order_by("name")
    serializer_class = SpecialtySerializer

class LevelListView(BaseListAPIView):
    queryset = Level.objects.all().order_by("name")
    serializer_class = LevelSerializer

class EducationFormListView(BaseListAPIView):
    queryset = EducationForm.objects.all().order_by("name")
    serializer_class = EducationFormSerializer

class EducationTypeListView(BaseListAPIView):
    queryset = EducationType.objects.all().order_by("name")
    serializer_class = EducationTypeSerializer

class PaymentFormListView(BaseListAPIView):
    queryset = PaymentForm.objects.all().order_by("name")
    serializer_class = PaymentFormSerializer

class StudentTypeListView(BaseListAPIView):
    queryset = StudentType.objects.all().order_by("name")
    serializer_class = StudentTypeSerializer

class SocialCategoryListView(BaseListAPIView):
    queryset = SocialCategory.objects.all().order_by("name")
    serializer_class = SocialCategorySerializer

class AccommodationListView(BaseListAPIView):
    queryset = Accommodation.objects.all().order_by("name")
    serializer_class = AccommodationSerializer

class CitizenshipListView(BaseListAPIView):
    queryset = Citizenship.objects.all().order_by("name")
    serializer_class = CitizenshipSerializer

class GenderListView(BaseListAPIView):
    queryset = Gender.objects.all().order_by("name")
    serializer_class = GenderSerializer

class ProvinceListView(BaseListAPIView):
    queryset = Province.objects.all().order_by("name")
    serializer_class = ProvinceSerializer

class DistrictListView(BaseListAPIView):
    queryset = District.objects.all().order_by("name")
    serializer_class = DistrictSerializer

class TerrainListView(BaseListAPIView):
    queryset = Terrain.objects.all().order_by("name")
    serializer_class = TerrainSerializer

class GroupListView(BaseListAPIView):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer

class SemesterListView(BaseListAPIView):
    queryset = Semester.objects.all().order_by("name")
    serializer_class = SemesterSerializer

class EducationYearListView(BaseListAPIView):
    queryset = EducationYear.objects.all().order_by("-current", "name")
    serializer_class = EducationYearSerializer
