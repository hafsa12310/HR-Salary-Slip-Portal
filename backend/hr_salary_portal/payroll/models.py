from django.db import models
from django.utils import timezone


class Employee(models.Model):
    emp_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    department = models.CharField(max_length=100, null=True)
    position = models.CharField(max_length=100, null=True)
    base_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    generated_at = models.DateTimeField(default=timezone.now, null=True)
    pdf = models.FileField(upload_to='salary_slips/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UploadLog(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    details = models.TextField()

    def __str__(self):
        return f"Upload on {self.uploaded_at} - Status: {self.status}"


class EmailLog(models.Model):
    employee = models.CharField(max_length=50)
    email = models.EmailField()
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Email to {self.email} on {self.timestamp} - Status: {self.status}"


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


from mongoengine import Document, StringField, DateTimeField
from django.utils import timezone

class Session(Document):
    session_key = StringField(required=True, unique=True)
    session_data = StringField(required=True)
    expire_date = DateTimeField(required=True)

    meta = {
        'collection': 'django_sessions',  # Name of the collection in MongoDB
        'indexes': [
            'expire_date',
        ]
    }


from mongoengine import Document, StringField, EmailField, BooleanField
from django.contrib.auth.hashers import make_password, check_password

class MyUser(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
