from django.contrib import admin
from core.modellar.student import (
    University, Department, Specialty, Level, EducationForm, EducationType,
    PaymentForm, StudentType, SocialCategory, Accommodation, Citizenship,
    Gender, Province, District, Terrain, Group, Semester, EducationYear, Student
)

# Override admin.site.get_app_list to group models in the sidebar
def get_custom_app_list(self, request):
    """
    Organizes models into three sections in the admin sidebar:
    - Students: Only Student model
    - Departments & Specialties: Department, Specialty
    - References: All other student-related models
    """
    app_list = self._build_app_dict(request)
    students_app = {
        'name': 'Students',
        'app_label': 'students',
        'app_url': '/admin/core/student/',
        'models': []
    }
    departments_app = {
        'name': 'Departments & Specialties',
        'app_label': 'departments',
        'app_url': '/admin/core/department/',
        'models': []
    }
    references_app = {
        'name': 'References',
        'app_label': 'references',
        'app_url': '/admin/core/university/',
        'models': []
    }
    
    for app in app_list.values():
        if app['app_label'] == 'core':
            for model in app['models']:
                model_name = model['object_name'].lower()
                if model_name == 'student':
                    students_app['models'].append(model)
                elif model_name in ['department', 'specialty']:
                    departments_app['models'].append(model)
                elif model_name in [
                    'university', 'level', 'educationform', 'educationtype', 'paymentform',
                    'studenttype', 'socialcategory', 'accommodation', 'citizenship',
                    'gender', 'province', 'district', 'terrain', 'group', 'semester', 'educationyear'
                ]:
                    references_app['models'].append(model)
    
    new_app_list = [
        app for app in app_list.values()
        if app['app_label'] != 'core'  # Keep non-core apps (e.g., auth)
    ]
    new_app_list.extend([students_app, departments_app, references_app])
    return new_app_list

# Patch the default admin.site
admin.site.get_app_list = get_custom_app_list.__get__(admin.site, admin.site.__class__)

# Register models with the default admin.site
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "university", "structure_type", "locality_type", "active")
    list_filter = ("university", "structure_type", "locality_type", "active")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department")
    list_filter = ("department",)
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)

@admin.register(EducationForm)
class EducationFormAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(EducationType)
class EducationTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(PaymentForm)
class PaymentFormAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(StudentType)
class StudentTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(SocialCategory)
class SocialCategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Citizenship)
class CitizenshipAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "province")
    list_filter = ("province",)
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "education_lang")
    search_fields = ("name", "education_lang")
    ordering = ("name",)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)

@admin.register(EducationYear)
class EducationYearAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "current")
    list_filter = ("current",)
    search_fields = ("code", "name")
    ordering = ("code",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "student_id_number",
        "university",
        "department",
        "specialty",
        "level",
        "education_form",
        "education_type",
        "payment_form",
        "gender",
        "avg_gpa",
        "total_credit",
        "is_graduate",
        "created_at",
    )
    search_fields = (
        "full_name",
        "first_name",
        "second_name",
        "third_name",
        "student_id_number",
        "email",
    )
    list_filter = (
        "university",
        "department",
        "specialty",
        "level",
        "education_form",
        "education_type",
        "payment_form",
        "student_type",
        "social_category",
        "accommodation",
        "gender",
        "citizenship",
        "province",
        "current_province",
        "is_graduate",
    )
    list_per_page = 25
    list_select_related = (
        "university", "department", "specialty", "level", "education_form",
        "education_type", "payment_form", "gender", "citizenship", "province",
        "current_province", "district", "current_district", "terrain", "current_terrain",
        "group", "semester", "education_year"
    )
    raw_id_fields = (
        "university", "department", "specialty", "level", "education_form",
        "education_type", "payment_form", "student_type", "social_category",
        "accommodation", "citizenship", "gender", "terrain", "current_terrain",
        "province", "current_province", "district", "current_district",
        "group", "semester", "education_year"
    )  # Removed 'country'
    fieldsets = (
        ("Personal Information", {
            "fields": (
                "full_name", "short_name", "first_name", "second_name", "third_name",
                "gender", "birth_date", "citizenship", "email", "student_id_number",
                "image", "image_full"
            )
        }),
        ("Academic Information", {
            "fields": (
                "university", "department", "specialty", "level", "education_form",
                "education_type", "payment_form", "student_type", "social_category",
                "accommodation", "group", "semester", "education_year", "year_of_enter",
                "avg_gpa", "avg_grade", "total_credit", "total_acload", "is_graduate"
            )
        }),
        ("Location Information", {
            "fields": (
                "country", "province", "current_province", "district", "current_district",
                "terrain", "current_terrain"
            )
        }),
        ("Additional Information", {
            "fields": (
                "meta_id", "roommate_count", "other", "hash", "validate_url",
                "created_at", "updated_at"
            )
        }),
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("full_name",)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['students_count'] = Student.objects.count()
        return super().changelist_view(request, extra_context=extra_context)