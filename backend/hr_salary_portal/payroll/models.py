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
    # pdf = models.FileField(upload_to='salary_slips/', null=True, blank=True)

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
