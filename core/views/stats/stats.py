from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count
from datetime import date
from core.modellar.student import Student

class StudentStatsAPIView(APIView):
    """
    Talabalar statistikasi API
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all students for stats
        students = Student.objects.filter(is_graduate=True)

        # 1️⃣ Jami talabalar soni
        total_students = students.count()

        # 2️⃣ Jins bo‘yicha
        # Assuming Gender model has a 'name' field (e.g., "Ayol", "Erkak")
        gender_stats = (
            students.values("gender__name")
            .annotate(count=Count("id"))
            .order_by("gender__name")
        )

        # 3️⃣ Bitiruvchi va bitirmaganlar
        graduate_stats = {
            "graduates": students.filter(is_graduate=True).count(),
            "non_graduates": students.filter(is_graduate=False).count(),
        }

        # 4️⃣ Yosh toifalari (bugungi sanadan hisoblanadi)
        age_groups = {"18-20": 0, "21-23": 0, "24+": 0, "unknown": 0}
        today = date.today()

        for s in students.only("birth_date"):
            if s.birth_date:
                age = today.year - s.birth_date.year - (
                    (today.month, today.day) < (s.birth_date.month, s.birth_date.day)
                )
                if 18 <= age <= 20:
                    age_groups["18-20"] += 1
                elif 21 <= age <= 23:
                    age_groups["21-23"] += 1
                elif age >= 24:
                    age_groups["24+"] += 1
                else:
                    age_groups["unknown"] += 1
            else:
                age_groups["unknown"] += 1

        # 5️⃣ Last 15 created students
        recent_students = Student.objects.select_related("specialty", "province", "district").filter(is_graduate=True).order_by("-created_at")[:15]
        recent_students_data = [
            {
                "id": student.id,
                "name": student.full_name,
                "field": student.specialty.name if student.specialty else "N/A",
                "province": student.province.name if student.province else "N/A",
                "district": student.district.name if student.district else "N/A",
                "status": "Ishli" if student.is_graduate else "Ishsiz",
                "date": student.created_at.strftime("%Y-%m-%d"),
            }
            for student in recent_students
        ]

        data = {
            "total_students": total_students,
            "gender_stats": list(gender_stats),
            "graduate_stats": graduate_stats,
            "age_groups": age_groups,
            "recent_students": recent_students_data,
        }

        return Response(data, status=status.HTTP_200_OK)