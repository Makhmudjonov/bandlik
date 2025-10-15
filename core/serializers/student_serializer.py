from rest_framework import serializers

from core.modellar.student import (
    University, Department, Specialty, Level, EducationForm, EducationType,
    PaymentForm, StudentType, SocialCategory, Accommodation, Citizenship,
    Gender, Province, District, Terrain, Group, Semester, EducationYear, Student)

class SimpleModelSerializer(serializers.ModelSerializer):
    """Umumiy serializer har qanday oddiy model uchun"""
    class Meta:
        model = None  # keyinchalik dinamik ishlatamiz
        fields = ["id", "name"]  # deyarli barcha modelda `name` bor

class StudentDetailSerializer(serializers.ModelSerializer):
    university = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    specialty = serializers.StringRelatedField()
    level = serializers.StringRelatedField()
    education_form = serializers.StringRelatedField()
    education_type = serializers.StringRelatedField()
    payment_form = serializers.StringRelatedField()
    student_type = serializers.StringRelatedField()
    social_category = serializers.StringRelatedField()
    accommodation = serializers.StringRelatedField()
    citizenship = serializers.StringRelatedField()
    gender = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    current_province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    current_district = serializers.StringRelatedField()
    terrain = serializers.StringRelatedField()
    current_terrain = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    semester = serializers.StringRelatedField()
    education_year = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = "__all__"


class SimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # placeholder (dynamic use only)
        fields = ["id", "name"]

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "code", "name"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "code", "name", "university"]

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "code", "name", "department"]

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "code", "name"]

class EducationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationForm
        fields = ["id", "code", "name"]

class EducationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationType
        fields = ["id", "code", "name"]

class PaymentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentForm
        fields = ["id", "code", "name"]

class StudentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentType
        fields = ["id", "code", "name"]

class SocialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialCategory
        fields = ["id", "code", "name"]

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ["id", "code", "name"]

class CitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = ["id", "code", "name"]

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ["id", "code", "name"]

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "code", "name"]

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "code", "name", "province"]

class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = ["id", "code", "name"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "education_lang"]

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ["id", "code", "name"]

class EducationYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationYear
        fields = ["id", "code", "name", "current"]
