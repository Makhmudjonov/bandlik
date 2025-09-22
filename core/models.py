from django.db import models
from django.contrib.auth.models import AbstractUser


class StudentData(models.Model):
    user = models.OneToOneField(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True,
    )
    university = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    hudud = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    jshshir = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    tashkilot = models.CharField(max_length=255, blank=True, null=True)
    lavozimi = models.CharField(max_length=255, blank=True, null=True)
    buyruq_sanasi = models.CharField(max_length=50, blank=True, null=True)
    bosqich = models.CharField(max_length=255, blank=True, null=True)
    yonalish = models.CharField(max_length=255, blank=True, null=True)
    is_worked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.tashkilot
        if not value:
            self.is_worked = False
        else:
            self.is_worked = True
        super().save(*args, **kwargs)


        def __str__(self):
            return f"{self.full_name} ({self.jshshir})"



class CustomUser(AbstractUser):
    """
    Username asosida login qilinadigan foydalanuvchi modeli.
    Email ixtiyoriy bo‘ladi.
    """
    email = models.EmailField(unique=False, blank=True, null=True)   # endi majburiy emas
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("student", "Student"),
        ("viewer", "Viewer"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")

    # username maydoni AbstractUser’da allaqachon bor
    USERNAME_FIELD = "username"      # 🔹 asosiy login maydoni — username
    REQUIRED_FIELDS = ["email", "full_name"]   # createsuperuser da qo‘shimcha so‘raladiganlar

    def __str__(self):
        return self.full_name or self.username