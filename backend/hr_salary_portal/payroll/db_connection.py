from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')  
db = client['hr_salary_portal_db']
