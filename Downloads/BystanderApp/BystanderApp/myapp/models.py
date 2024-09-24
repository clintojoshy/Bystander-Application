from django.db import models
from django.contrib.auth.hashers import make_password

USER_TYPE_CHOICES = (
    ("Patient", "Patient"),
    ("Bystander", "Bystander"),
)

class User(models.Model):
    first_name = models.CharField(max_length=50)  # First Name
    last_name = models.CharField(max_length=50)   # Last Name
    gender = models.CharField(max_length=10, choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")))
    address = models.TextField(blank=True, null=True)  # Made nullable
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Increased length for hashed passwords
    phone = models.CharField(max_length=15)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Updated to show full name

    class Meta:
        verbose_name_plural = "Users"  # Optional: plural name for the admin panel

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class MedicalHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Patient'})
    condition = models.CharField(max_length=100)
    date_diagnosed = models.DateField()
    medications = models.TextField(blank=True, null=True)  # Made nullable
    notes = models.TextField(blank=True, null=True)  # Made nullable

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Recovered", "Recovered"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.condition}"

    class Meta:
        verbose_name_plural = "Medical Histories"  # Optional: plural name for the admin panel
        ordering = ['-date_diagnosed']  # Optional: default ordering by diagnosis date


class Admin(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Admins"  # Optional: plural name for the admin panel
