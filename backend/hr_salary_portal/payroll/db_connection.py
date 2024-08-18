import pymongo

url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(url)

db = client ['hr_salary_portal_db']