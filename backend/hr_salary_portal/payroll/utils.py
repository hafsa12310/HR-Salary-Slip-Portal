from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

# Initialize MongoDB client
client = MongoClient(settings.MONGO_URI)
db = client['hr_salary_portal_db']

def log_email(employee_id, email, status, details=None):
    try:
        print(f"Logging email for {employee_id} with status: {status}")  # Add this line
        log_entry = {
            "employee": employee_id,
            "email": email,
            "status": status,
            "timestamp": datetime.now(),
            "details": details
        }
        db.email_log.insert_one(log_entry)
    except Exception as e:
        print(f"Failed to log email for {employee_id}: {str(e)}")

