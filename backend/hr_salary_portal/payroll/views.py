from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import pandas as pd
from django.http import HttpResponse, FileResponse
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from payroll.template import draw_payslip_layout
import io
import zipfile
from django.core.mail import EmailMessage
from django.conf import settings
from payroll.db_connection import db
from django.core.mail import EmailMessage
from django.conf import settings
from hr_salary_portal.settings import db
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import log_email
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class UploadFileView(APIView):
    permission_classes = []  
    authentication_classes = []
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            collection = db['payroll_employee']

            for _, row in df.iterrows():
                employee_data = {
                    'month' : row.get('month'),
                    'emp_id': row.get('emp_id'),
                    'first_name': row.get('first_name'),
                    'last_name': row.get('last_name'),
                    'email': row.get('email'),
                    'department': row.get('department'),
                    'position': row.get('position'),
                    'base_pay': row.get('base_pay', 0.00),
                    'allowances': row.get('allowances', 0.00),
                    'deductions': row.get('deductions', 0.00),
                    'net_salary': row.get('net_salary', 0.00),
                
                }

                existing_employee = collection.find_one(
                    {"emp_id": employee_data['emp_id'], "email": employee_data['email']}
                )

                if existing_employee:
                    try:
                        collection.update_one(
                            {"emp_id": employee_data['emp_id'], "email": employee_data['email']},
                            {"$set": employee_data}
                        )
                        print(f"Employee with emp_id {employee_data['emp_id']} updated successfully in MongoDB.")
                    except Exception as e:
                        print(f"Error updating data in MongoDB: {str(e)}")
                        return Response({"error": f"Error updating data in MongoDB: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        collection.insert_one(employee_data)
                        print(f"Employee with emp_id {employee_data['emp_id']} inserted successfully into MongoDB.")
                    except Exception as e:
                        print(f"Error inserting data into MongoDB: {str(e)}")
                        return Response({"error": f"Error inserting data into MongoDB: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "File processed and data inserted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GeneratePDFView(APIView):
    permission_classes = []  
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        try:
            # Get all employees from MongoDB
            employees = list(db['payroll_employee'].find())

            if len(employees) == 0:
                return Response({"message": "No employees found in the database"}, status=status.HTTP_404_NOT_FOUND)

            for employee in employees:
                generate_salary_slip_pdf(employee['emp_id'])

            return Response({"message": "Payslips generated for all employees"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def generate_salary_slip_pdf(employee_id):
    permission_classes = []  
    authentication_classes = []
    directory = 'PaySlips'
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{directory}': {e}")
            return HttpResponse(f"Error creating directory '{directory}': {e}", status=500)

    employee = db['payroll_employee'].find_one({'emp_id': employee_id})

    if not employee:
        return HttpResponse("Employee not found", status=404)

    print(f"Retrieved Employee Data: {employee}")

    file_path = os.path.join(directory, f'salary_slip_{employee_id}.pdf')

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    logo_path = "C:/Users/sarmaaya/Desktop/new/HR-Salary-Slip-Portal/backend/hr_salary_portal/logo.png"
    draw_payslip_layout(c, employee, width, height, logo_path)

    c.save()

    print(f"Generated PDF for employee {employee_id} at {file_path}")


class DownloadPayslipsView(APIView):
    permission_classes = []  
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        try:
            directory = 'PaySlips'

            if not os.path.exists(directory):
                return Response({"error": "No payslips found to download."}, status=status.HTTP_404_NOT_FOUND)

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    zip_file.write(file_path, os.path.basename(file_path))

            zip_buffer.seek(0)

            response = FileResponse(zip_buffer, as_attachment=True, filename="payslips.zip")
            return response

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendPayslipsView(APIView):
    permission_classes = []  
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        try:
            employees = list(db['payroll_employee'].find())
            if len(employees) == 0:
                return Response({"message": "No employees found in the database"}, status=status.HTTP_404_NOT_FOUND)

            directory = 'PaySlips'
            log_details = []

            for employee in employees:
                email = employee.get('email')
                first_name = employee.get('first_name')
                last_name = employee.get('last_name')
                emp_id = employee.get('emp_id')
                month = employee.get('month')
                file_path = os.path.join(directory, f'salary_slip_{emp_id}.pdf')

                if os.path.exists(file_path):
                    try:
                        mail = EmailMessage(
                            subject=f"Payslip for the month of - {month}",
                            body=(
                                "Please find your Payslip attached. In case of any discrepancies, contact HR for support."
                                "\n"
                                "\n"
                                "This email and any attachments are confidential and intended only for the individual named. "
                                "If you are not the named addressee you should not disseminate, distribute or copy this email. "
                                "Please notify the sender immediately by email if you have received this email by mistake and delete this email from your system."
                            ),
                            from_email=settings.EMAIL_HOST_USER,
                            to=[email],
                        )
                        mail.attach_file(file_path)
                        mail.send()

                        log_message = f"Email sent to {first_name} {last_name} with status: Sent"
                        log_email(emp_id, email, "Sent", f"Payslip sent to {email} successfully.")

                    except Exception as e:
                        log_message = f"Failed to send email to {email}: {str(e)}"
                        log_email(emp_id, email, "Failed", str(e))
                else:
                    log_message = f"Payslip file {file_path} not found for {emp_id}"
                    log_email(emp_id, email, "Failed", f"Payslip file {file_path} not found.")

                print(log_message)
                log_details.append(log_message)

            return Response({"message": "Emails processed.", "log_details": log_details}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


def landing_page_view(request):
    return render(request, 'landing.html')



# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MyUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegisterView(APIView):
    permission_classes = [] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

        if MyUser.objects(email=email).first():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = MyUser(email=email)
        user.set_password(password)
        user.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MyUser

class LoginView(APIView):
    permission_classes = []  
    authentication_classes = []  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = MyUser.objects(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

