from django.db import models

class Employee(models.Model):
    emp_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class SalarySlip(models.Model):
    employee = models.ForeignKey(Employee, to_field='emp_id', on_delete=models.CASCADE)
    base_pay = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='salary_slips/')

    def __str__(self):
        return f"Salary Slip for {self.employee.first_name} {self.employee.last_name} - {self.generated_at}"


class UploadLog(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    details = models.TextField()

    def __str__(self):
        return f"Upload on {self.uploaded_at} - Status: {self.status}"
