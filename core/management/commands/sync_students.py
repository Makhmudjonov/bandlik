import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from core.modellar.student import *

class Command(BaseCommand):
    help = "HEMIS student ma'lumotlarini to‘liq sinxronlashtiradi."

    def handle(self, *args, **options):
        base_url = "https://student.tashmeduni.uz/rest/v1/data/student-list"
        token = "beaBtgoJshycmtSraSC8QIXEFIpRvXuI"
        headers = {"Authorization": f"Bearer {token}"}
        page = 1
        total = 0

        while True:
            url = f"{base_url}?limit=200&page={page}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"API error: {response.status_code}"))
                break

            data = response.json()
            items = data.get("data", {}).get("items", [])
            if not items:
                break

            with transaction.atomic():
                for item in items:
                    # --- Yordamchi ma'lumotlarni olish ---
                    university_data = item.get("university")
                    department_data = item.get("department")
                    specialty_data = item.get("specialty")
                    level_data = item.get("level")
                    edu_form_data = item.get("educationForm")
                    edu_type_data = item.get("educationType")
                    payment_form_data = item.get("paymentForm")
                    student_type_data = item.get("studentType")
                    social_category_data = item.get("socialCategory")
                    accommodation_data = item.get("accommodation")
                    gender_data = item.get("gender")
                    citizenship_data = item.get("citizenship")
                    terrain_data = item.get("terrain")
                    current_terrain_data = item.get("currentTerrain")
                    province_data = item.get("province")
                    cur_province_data = item.get("currentProvince")
                    district_data = item.get("district")
                    cur_district_data = item.get("currentDistrict")
                    group_data = item.get("group")
                    semester_data = item.get("semester")
                    education_year_data = item.get("educationYear")

                    # --- Obyektlarni yaratish yoki olish ---
                    university = department = specialty = level = education_form = None
                    education_type = payment_form = student_type = social_category = None
                    accommodation = gender = citizenship = terrain = current_terrain = None
                    province = current_province = district = current_district = None
                    group = semester = education_year = None

                    if university_data:
                        university, _ = University.objects.update_or_create(
                            code=university_data["code"],
                            defaults={"name": university_data["name"]}
                        )

                    if department_data and university:
                        department, _ = Department.objects.update_or_create(
                            code=department_data["code"],
                            defaults={
                                "name": department_data["name"],
                                "university": university,
                                "structure_type": department_data.get("structureType", {}).get("code"),
                                "locality_type": department_data.get("localityType", {}).get("code"),
                                "active": department_data.get("active", True)
                            }
                        )

                    if specialty_data and department:
                        specialty, _ = Specialty.objects.get_or_create(
                            code=specialty_data["code"],
                            defaults={"name": specialty_data["name"], "department": department}
                        )

                    if level_data:
                        level, _ = Level.objects.get_or_create(
                            code=level_data["code"],
                            defaults={"name": level_data["name"]}
                        )

                    if edu_form_data:
                        education_form, _ = EducationForm.objects.get_or_create(
                            code=edu_form_data["code"],
                            defaults={"name": edu_form_data["name"]}
                        )

                    if edu_type_data:
                        education_type, _ = EducationType.objects.get_or_create(
                            code=edu_type_data["code"],
                            defaults={"name": edu_type_data["name"]}
                        )

                    if payment_form_data:
                        payment_form, _ = PaymentForm.objects.get_or_create(
                            code=payment_form_data["code"],
                            defaults={"name": payment_form_data["name"]}
                        )

                    if student_type_data:
                        student_type, _ = StudentType.objects.get_or_create(
                            code=student_type_data["code"],
                            defaults={"name": student_type_data["name"]}
                        )

                    if social_category_data:
                        social_category, _ = SocialCategory.objects.get_or_create(
                            code=social_category_data["code"],
                            defaults={"name": social_category_data["name"]}
                        )

                    if accommodation_data:
                        accommodation, _ = Accommodation.objects.get_or_create(
                            code=accommodation_data["code"],
                            defaults={"name": accommodation_data["name"]}
                        )

                    if gender_data:
                        gender, _ = Gender.objects.get_or_create(
                            code=gender_data["code"],
                            defaults={"name": gender_data["name"]}
                        )

                    if citizenship_data:
                        citizenship, _ = Citizenship.objects.get_or_create(
                            code=citizenship_data["code"],
                            defaults={"name": citizenship_data["name"]}
                        )

                    if terrain_data:
                        terrain, _ = Terrain.objects.get_or_create(
                            code=terrain_data["code"],
                            defaults={"name": terrain_data["name"]}
                        )

                    if current_terrain_data:
                        current_terrain, _ = Terrain.objects.get_or_create(
                            code=current_terrain_data["code"],
                            defaults={"name": current_terrain_data["name"]}
                        )

                    if province_data:
                        province, _ = Province.objects.get_or_create(
                            code=province_data["code"],
                            defaults={"name": province_data["name"]}
                        )

                    if cur_province_data:
                        current_province, _ = Province.objects.get_or_create(
                            code=cur_province_data["code"],
                            defaults={"name": cur_province_data["name"]}
                        )

                    if district_data and province:
                        district, _ = District.objects.get_or_create(
                            code=district_data["code"],
                            defaults={"name": district_data["name"], "province": province}
                        )

                    if cur_district_data and current_province:
                        current_district, _ = District.objects.get_or_create(
                            code=cur_district_data["code"],
                            defaults={"name": cur_district_data["name"], "province": current_province}
                        )

                    if group_data:
                        group, _ = Group.objects.get_or_create(
                            id=group_data["id"],
                            defaults={
                                "name": group_data["name"],
                                "education_lang": group_data.get("educationLang", {}).get("code")
                            }
                        )

                    if semester_data:
                        semester, _ = Semester.objects.get_or_create(
                            code=semester_data["code"],
                            defaults={"name": semester_data["name"]}
                        )

                    if education_year_data:
                        education_year, _ = EducationYear.objects.get_or_create(
                            code=education_year_data["code"],
                            defaults={"name": education_year_data["name"], "current": education_year_data.get("current", False)}
                        )

                    # --- Tug‘ilgan sanani parse qilish ---
                    try:
                        birth_date = datetime.fromtimestamp(item["birth_date"]).date()
                    except Exception:
                        birth_date = None

                    # --- Yaratilgan va yangilangan sanani parse qilish ---
                    try:
                        created_at = datetime.fromtimestamp(item["created_at"])
                    except Exception:
                        created_at = None

                    try:
                        updated_at = datetime.fromtimestamp(item["updated_at"])
                    except Exception:
                        updated_at = None


                    country = "Uzbekistan"  # Default value
                    if citizenship_data and isinstance(citizenship_data, dict):
                        country = citizenship_data.get("name", "Uzbekistan")
                    elif item.get("country"):
                        country = item.get("country") if isinstance(item.get("country"), str) else "Uzbekistan"

                    # --- Studentni yaratish yoki yangilash ---
                    Student.objects.update_or_create(
                        id=item["id"],
                        defaults={
                            "meta_id": item.get("meta_id"),
                            "university": university,
                            "department": department,
                            "specialty": specialty,
                            "level": level,
                            "education_form": education_form,
                            "education_type": education_type,
                            "payment_form": payment_form,
                            "student_type": student_type,
                            "social_category": social_category,
                            "accommodation": accommodation,
                            "citizenship": citizenship,
                            "gender": gender,
                            "terrain": terrain,
                            "current_terrain": current_terrain,
                            "country": country,  # Use API data or default to "Uzbekistan"
                            "province": province,
                            "current_province": current_province,
                            "district": district,
                            "current_district": current_district,
                            "group": group,
                            "semester": semester,
                            "education_year": education_year,
                            "full_name": item.get("full_name", ""),
                            "short_name": item.get("short_name", ""),
                            "first_name": item.get("first_name", ""),
                            "second_name": item.get("second_name", ""),
                            "third_name": item.get("third_name"),
                            "birth_date": birth_date,
                            "student_id_number": item.get("student_id_number"),
                            "year_of_enter": item.get("year_of_enter"),
                            "is_graduate": item.get("is_graduate", False),
                            "avg_gpa": item.get("avg_gpa", 0),
                            "avg_grade": item.get("avg_grade", 0),
                            "total_credit": item.get("total_credit", 0),
                            "total_acload": item.get("total_acload", 0),
                            "roommate_count": item.get("roommate_count"),
                            "other": item.get("other", ""),
                            "image": item.get("image", ""),
                            "image_full": item.get("image_full", ""),
                            "email": item.get("email", ""),
                            "hash": item.get("hash", ""),
                            "validate_url": item.get("validateUrl", ""),
                            "created_at": created_at,
                            "updated_at": updated_at,
                        }
                    )
                    total += 1

            self.stdout.write(self.style.SUCCESS(f"✅ Sahifa {page}: {len(items)} ta student"))
            if page >= data["data"]["pagination"]["pageCount"]:
                break
            page += 1

        self.stdout.write(self.style.SUCCESS(f"🎓 Hammasi tugadi. {total} ta student saqlandi."))