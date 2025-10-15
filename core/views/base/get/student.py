from core.modellar.student import Student
from core.serializers.student_serializer import StudentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StudentPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"


class StudentListView(generics.ListAPIView):
    """
    Talabalar ro'yxati (to‘liq ma'lumot bilan)
    Misol:
    /api/students/list/?department=1&level=3&gender=Erkak&province=14
    """
    queryset = (
        Student.objects.filter(is_graduate=True).select_related(
            "university", "department", "specialty", "level",
            "education_form", "education_type", "payment_form",
            "student_type", "social_category", "accommodation",
            "citizenship", "gender", "province", "current_province",
            "district", "current_district", "terrain", "current_terrain",
            "group", "semester", "education_year"
        ).order_by("full_name")
    )
    serializer_class = StudentDetailSerializer
    pagination_class = StudentPagination
    permission_classes = [permissions.IsAuthenticated]

    # 🔹 Filterlar
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["full_name", "student_id_number"]
    filterset_fields = {
        "department": ["exact"],
        "specialty": ["exact"],
        "level": ["exact"],
        "gender": ["exact"],
        "province": ["exact"],
        "current_province": ["exact"],
        "social_category": ["exact"],
        "accommodation": ["exact"],
        "payment_form": ["exact"],
        "education_form": ["exact"],
        "education_type": ["exact"],
        "student_type": ["exact"],
        "is_graduate": ["exact"],
    }

    # ✅ Swagger parametrlari — to‘g‘ri joyda (list metodida)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("search", openapi.IN_QUERY, description="Talaba F.I.Sh yoki ID bo‘yicha qidiruv", type=openapi.TYPE_STRING),
            openapi.Parameter("department", openapi.IN_QUERY, description="Fakultet ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("specialty", openapi.IN_QUERY, description="Yo‘nalish ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("level", openapi.IN_QUERY, description="Kurs ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("gender", openapi.IN_QUERY, description="Jinsi (Erkak/Ayol)", type=openapi.TYPE_STRING),
            openapi.Parameter("province", openapi.IN_QUERY, description="Asl viloyat ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("current_province", openapi.IN_QUERY, description="Hozirgi yashash viloyat ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("social_category", openapi.IN_QUERY, description="Ijtimoiy toifa ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("accommodation", openapi.IN_QUERY, description="Turar joy ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("payment_form", openapi.IN_QUERY, description="To‘lov turi ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("education_form", openapi.IN_QUERY, description="Ta’lim shakli ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("education_type", openapi.IN_QUERY, description="Ta’lim turi ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("is_graduate", openapi.IN_QUERY, description="Bitiruvchi (true/false)", type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Talabalar ro'yxatini olish (filterlar bilan)
        """
        return super().list(request, *args, **kwargs)
