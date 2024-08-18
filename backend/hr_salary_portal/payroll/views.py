from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from payroll.db_connection import db  # Import the MongoDB connection
from django.http import HttpResponse
import os

class UploadFileView(APIView):
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

                # Check if the employee exists in MongoDB
                existing_employee = collection.find_one({"emp_id": employee_data['emp_id'], "email": employee_data['email']})

                if existing_employee:
                    # If employee exists, update the record
                    try:
                        collection.update_one(
                            {"emp_id": employee_data['emp_id'], "email": employee_data['email']},
                            {"$set": employee_data}
                        )
                        print(f"Employee with emp_id {employee_data['emp_id']} updated successfully in MongoDB.")
                    except Exception as e:
                        print("Error updating data in MongoDB:", str(e))
                        return Response({"error": f"Error updating data in MongoDB: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # If employee does not exist, insert a new record
                    try:
                        collection.insert_one(employee_data)
                        print(f"Employee with emp_id {employee_data['emp_id']} inserted successfully into MongoDB.")
                    except Exception as e:
                        print("Error inserting data into MongoDB:", str(e))
                        return Response({"error": f"Error inserting data into MongoDB: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

                # Generate the salary slip PDF after saving employee data
                generate_salary_slip_pdf(employee_data['emp_id'])

            return Response({"message": "File processed and data inserted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Exception occurred:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def generate_salary_slip_pdf(employee_id):
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

    print("Retrieved Employee Data:", employee)

    file_path = os.path.join(directory, f'salary_slip_{employee_id}.pdf')

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Draw the content on the PDF using the fields from the Employee model
    c.drawString(100, height - 100, f"Salary Slip for {employee['first_name']} {employee['last_name']}")
    c.drawString(100, height - 150, f"Employee ID: {employee['emp_id']}")
    c.drawString(100, height - 200, f"Base Pay: {employee.get('base_pay', 0.00)}")
    c.drawString(100, height - 250, f"Allowances: {employee.get('allowances', 0.00)}")
    c.drawString(100, height - 300, f"Deductions: {employee.get('deductions', 0.00)}")
    c.drawString(100, height - 350, f"Net Salary: {employee.get('net_salary', 0.00)}")

    # Save the PDF in the specified directory
    c.save()

    print(f"Generated PDF for employee {employee_id} at {file_path}")