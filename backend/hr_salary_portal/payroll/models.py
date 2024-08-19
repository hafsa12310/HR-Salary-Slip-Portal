from django.db import models


class Employee(models.Model):
    onth = models.CharField(max_length=50)
    emp_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    base_pay = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='salary_slips/')

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
