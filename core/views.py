import json
from django.views import View
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import StudentData
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken





from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.files.storage import default_storage
import json
from rest_framework.permissions import IsAuthenticated, AllowAny


from core.models import StudentData


class UploadStudentJSONView(APIView):
    permission_classes = [IsAuthenticated]

    """
    JSON fayl yuklab, talabalar ma'lumotlarini bazaga yozish.
    """

    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="JSON fayl yuklab, talabalar ma'lumotlarini saqlash",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                description="Talabalar ro‘yxati JSON fayl ko‘rinishida",
                type=openapi.TYPE_FILE,
                required=True,
            )
        ],
        responses={200: "OK", 400: "Xatolik"}
    )
    def post(self, request, *args, **kwargs):
        """
        1) Foydalanuvchi JSON fayl yuklaydi.
        2) Faylni ochib, ma'lumotlarni StudentData jadvaliga yozadi.
        """
        json_file = request.FILES.get("file")
        if not json_file:
            return Response({"error": "Fayl yuklanmadi"}, status=400)

        # Faylni vaqtinchalik saqlaymiz
        file_path = default_storage.save(f"tmp/{json_file.name}", json_file)

        try:
            # Faylni ochish (binary rejimda) va dekodlash
            with default_storage.open(file_path, "rb") as f:
                raw = f.read().decode("utf-8")
                data = json.loads(raw)

            def prepare_student(item: dict) -> StudentData:
                """
                JSON ichidagi bitta yozuvdan StudentData obyektini yaratish.
                """
                tashkilot_value = item.get("tashkilot")
                is_worked = False
                if tashkilot_value not in (None, ""):
                    is_worked = True

                return StudentData(
                    full_name=item.get("full_name", ""),
                    jshshir=item.get("jshshir", ""),
                    tashkilot=tashkilot_value,
                    university=item.get("university"),
                    hudud=item.get("hudud"),
                    region=item.get("region"),
                    specialty=item.get("specialty"),
                    lavozimi=item.get("lavozimi"),
                    buyruq_sanasi=item.get("buyruq_sanasi"),
                    bosqich=item.get("bosqich"),
                    yonalish=item.get("yonalish"),
                    is_worked=is_worked,
                )

            # Bir nechta yozuv bo‘lsa — ro‘yxat sifatida keladi
            if isinstance(data, list):
                objs = [prepare_student(item) for item in data]
                StudentData.objects.bulk_create(objs, ignore_conflicts=True)
            else:
                StudentData.objects.create(**prepare_student(data).__dict__)

            return Response({"success": True})

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        finally:
            # Faylni o‘chirib tashlaymiz
            default_storage.delete(file_path)


class StudentStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    Talabalar statistikasi:
    - Jami ishlayotgan / ishsizlar
    - Eng ko‘p ish beruvchi tashkilotlar
    - Hududlar bo‘yicha
    - Tashkilot va mutaxassisliklar (specialty) bo‘yicha
    """

    # --- Umumiy studentlar statistikasi
    def get_total_stats(self, qs):
        total = qs.count()
        worked = qs.filter(is_worked=True).count()
        unemployed = total - worked
        return {
            "total": total,
            "worked": worked,
            "unemployed": unemployed,
            "worked_percent": round(worked / total * 100, 1) if total else 0,
            "unemployed_percent": round(unemployed / total * 100, 1) if total else 0,
        }

    # --- Eng ko‘p ish beruvchi tashkilotlar
    def get_top_employers(self, qs, limit=20):
        return list(
            qs.filter(is_worked=True)
            .values("tashkilot")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )

    # --- Hududlar bo‘yicha
    def get_hudud_stats(self, qs):
        hududlar = (
            qs.values("hudud")
            .annotate(total=Count("id"), worked=Count("id", filter=Q(is_worked=True)))
            .order_by("-total")
        )
        result = []
        for h in hududlar:
            total = h["total"]
            worked = h["worked"]
            result.append(
                {
                    "hudud": h["hudud"],
                    "total": total,
                    "worked": worked,
                    "unemployed": total - worked,
                    "worked_percent": round(worked / total * 100, 1) if total else 0,
                }
            )
        return result

    # --- Mutaxassislik (specialty) kesimida
    def get_specialty_stats(self, qs):
        specialties = (
            qs.values("specialty")
            .annotate(total=Count("id"), worked=Count("id", filter=Q(is_worked=True)))
            .order_by("-total")
        )
        for s in specialties:
            s["unemployed"] = s["total"] - s["worked"]
            s["worked_percent"] = (
                round(s["worked"] / s["total"] * 100, 1) if s["total"] else 0
            )
        return list(specialties)

    # --- GET metodi
    def get(self, request):
        qs = StudentData.objects.all()

        data = {
            "summary": self.get_total_stats(qs),
            "top_employers": self.get_top_employers(qs),
            "hudud": self.get_hudud_stats(qs),
            "specialties": self.get_specialty_stats(qs),
        }
        return Response(data)
    

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    """
    Foydalanuvchini login qilish.
    Body (POST):
    {
        "username": "user1",
        "password": "12345"
    }
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username va parol kiritilishi kerak"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Login yoki parol noto‘g‘ri"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        # StudentData bilan bog‘lanishni tekshiramiz
        student_info = None
        try:
            student = StudentData.objects.get(user=user)
            student_info = {
                "university": student.university,
                "full_name": student.full_name,
                "hudud": student.hudud,
                "region": student.region,
                "jshshir": student.jshshir,
                "specialty": student.specialty,
                "tashkilot": student.tashkilot,
                "lavozimi": student.lavozimi,
                "bosqich": student.bosqich,
                "yonalish": student.yonalish,
                "is_worked": student.is_worked,
            }
        except StudentData.DoesNotExist:
            pass

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": getattr(user, "full_name", None),
                    "phone": getattr(user, "phone", None),
                    "role": user.role,
                },
                "student_profile": student_info,
            },
            status=status.HTTP_200_OK,
        )