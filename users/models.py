from django.contrib.auth.models import AbstractUser
from django.db import models as m
from cloudinary.models import CloudinaryField


# =========================
# Upload Path Functions
# =========================

def user_resume_path(instance, filename):
    return f"user_{instance.user.id}/resumes/{filename}"

def user_photo_path(instance, filename):
    return f"user_{instance.user.id}/photos/{filename}"


# =========================
# Custom User Model
# =========================

class User(AbstractUser):
    PROFILE_CHOICES = (
        ('employer', 'Employer'),
        ('seeker', 'Seeker'),
    )

    email = m.EmailField(unique=True)
    profile = m.CharField(max_length=20, choices=PROFILE_CHOICES, null=True, blank=True)
    is_profile_completed = m.BooleanField(default=False)

    def __str__(self):
        return self.username


# =========================
# Seeker Profile
# =========================

class SeekerProfile(m.Model):

    user = m.OneToOneField(
        User,
        related_name="seeker_profile",
        on_delete=m.CASCADE
    )

    mobile = m.CharField(max_length=15, unique=True)
    country_code = m.CharField(max_length=10)

    country = m.CharField(max_length=50)
    state = m.CharField(max_length=50)
    city = m.CharField(max_length=50)
    locality = m.CharField(max_length=50)

    preferred_job = m.CharField(max_length=100)
    experience = m.CharField(max_length=50)

    qualification = m.CharField(max_length=50)
    degree = m.CharField(max_length=100)
    college = m.CharField(max_length=150)
    year_of_passing = m.IntegerField()

    resume = CloudinaryField('resume', resource_type='raw', blank=True, null=True)
    photo = CloudinaryField('photo', blank=True, null=True)

    relocate = m.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Seeker Profile"


# =========================
# Employer Profile
# =========================

class EmployerProfile(m.Model):

    user = m.OneToOneField(
        User,
        related_name="employer_profile",
        on_delete=m.CASCADE
    )

    mobile = m.CharField(max_length=15)
    country_code = m.CharField(max_length=10)
    role = m.CharField(max_length=50)

    photo = m.ImageField(upload_to="employer/photos/", blank=True, null=True)
    company_logo = m.ImageField(upload_to="employer/logos/", blank=True, null=True)

    company_name = m.CharField(max_length=100)

    COMPANY_CHOICES = (
        ('startup', 'Startup'),
        ('mnc', 'MNC'),
        ('consultancy', 'Consultancy'),
    )

    company_type = m.CharField(max_length=50, choices=COMPANY_CHOICES)
    company_size = m.CharField(max_length=50)

    office_city = m.CharField(max_length=50)
    office_address = m.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.user.username} - Employer Profile"
    
class Interview(m.Model):

    employer = m.ForeignKey(EmployerProfile, on_delete=m.CASCADE)

    job_title = m.CharField(max_length=100)
    experience = m.CharField(max_length=30)
    job_type = m.CharField(max_length=30)
    qualification = m.CharField(max_length=500)
    job_mode = m.CharField(max_length=50)
    why_join_us = m.TextField()
    application_link = m.URLField()

    start_date = m.DateField()
    end_date = m.DateField(null=True, blank=True)
    time = m.TimeField()  
    venue = m.CharField(max_length=200)

    contact_phone = m.CharField(max_length=15)
    contact_email = m.EmailField()

    poster = m.ImageField(upload_to='employer/posters/', null=True, blank=True)

    created_at = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

class Comments(m.Model):
   seeker=m.ForeignKey(SeekerProfile,on_delete=m.CASCADE)
   interview=m.ForeignKey(Interview, on_delete=m.CASCADE)
   comment=m.TextField()
   created_at=m.DateTimeField(auto_now_add=True)
   
   def __str__(self):
        return f"{self.seeker.user.username} - {self.interview.job_role}"
    
class Like(m.Model):
    seeker = m.ForeignKey(SeekerProfile, on_delete=m.CASCADE)
    interview = m.ForeignKey(Interview, on_delete=m.CASCADE)
    created_at = m.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seeker', 'interview')