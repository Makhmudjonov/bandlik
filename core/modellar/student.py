from django.db import models

class University(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="departments")
    structure_type = models.CharField(max_length=10, blank=True, null=True)
    locality_type = models.CharField(max_length=10, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="specialties")

    def __str__(self):
        return self.name

class Level(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationForm(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PaymentForm(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SocialCategory(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Citizenship(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Gender(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Province(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class District(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, related_name="districts")

    def __str__(self):
        return self.name

class Terrain(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    education_lang = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationYear(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    meta_id = models.IntegerField(null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)  # Keep non-nullable
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    education_form = models.ForeignKey('EducationForm', on_delete=models.CASCADE)
    education_type = models.ForeignKey('EducationType', on_delete=models.CASCADE)
    payment_form = models.ForeignKey('PaymentForm', on_delete=models.CASCADE)
    student_type = models.ForeignKey('StudentType', on_delete=models.CASCADE, null=True, blank=True)
    social_category = models.ForeignKey('SocialCategory', on_delete=models.CASCADE, null=True, blank=True)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE, null=True, blank=True)
    citizenship = models.ForeignKey('Citizenship', on_delete=models.CASCADE)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, null=True, blank=True)
    current_province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='current_province_students', null=True, blank=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE, null=True, blank=True)
    current_district = models.ForeignKey('District', on_delete=models.CASCADE, related_name='current_district_students', null=True, blank=True)
    terrain = models.ForeignKey('Terrain', on_delete=models.CASCADE, null=True, blank=True)
    current_terrain = models.ForeignKey('Terrain', on_delete=models.CASCADE, related_name='current_terrain_students', null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=True, blank=True)
    education_year = models.ForeignKey('EducationYear', on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    third_name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    student_id_number = models.CharField(max_length=50, unique=True)
    image = models.URLField(null=True, blank=True)
    image_full = models.URLField(null=True, blank=True)
    year_of_enter = models.IntegerField(null=True, blank=True)
    avg_gpa = models.FloatField(null=True, blank=True)
    avg_grade = models.FloatField(null=True, blank=True)
    total_credit = models.IntegerField(null=True, blank=True)
    total_acload = models.IntegerField(null=True, blank=True)  # Made nullable
    is_graduate = models.BooleanField(default=False)
    roommate_count = models.IntegerField(null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    hash = models.CharField(max_length=255, null=True, blank=True)
    validate_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.full_name