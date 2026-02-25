import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import sqlite3
import pandas as pd

city = input("What city would you like to search from? ").title()

choice = input("(Choose option 1 or 2)\nWould like to see\n1. What your pay will be with your current skills\n2. What skills have the most pay in general\n")
data = []
data1 = []

if choice == '1':
    skills = input("Input your current skill(s)(if plural separate by a space): ").title()
    for i in range(1,6):
        url = f"http://api.adzuna.com/v1/api/jobs/gb/search/{i}?app_id=bbb231a1&app_key=ead6a75aff389175119f5fc5fd7d97cc&content-type=application/json"
        query_params = {
            "what_or": skills,
            "where": city
        }
        response = requests.get(url, params=query_params)
        json = response.json()
        data.append(json)

        time.sleep(2)
        

if choice == '2':
    skills = ["Python", "SQL", "Machine Learning", "AWS", "Java","JavaScript","C++","CSS","HTML","MATLAB","AI"]
    search_terms = "data, software, web development, engineer, tech"
    for i in range(1,6):
        url = f"http://api.adzuna.com/v1/api/jobs/gb/search/{i}?app_id=bbb231a1&app_key=ead6a75aff389175119f5fc5fd7d97cc&content-type=application/json"
        query_params = {
            "what_or": search_terms,
            "where": city
        }
        response = requests.get(url, params=query_params)
        json = response.json()
        data1.extend(json['results'])

        time.sleep(2)
    
    total_skill_counts = Counter()
    skill_pattern = r'\b(' + '|'.join(map(re.escape, skills)) + r')\b'
    for entry in data1:
        text = entry.get('description', "")
        if text:
            matches = re.findall(skill_pattern, text, flags=re.IGNORECASE)
            normalized_matches = [m for m in matches]
            total_skill_counts.update(normalized_matches)

try:
    dataframe = pd.DataFrame(total_skill_counts.items(), columns=['Skill', 'Count'])
    dataframe
except NameError:
    print("~~~~~~~~~Data Loaded Successfully~~~~~~~~~")

try:
    min_list = []
    max_list = []
    jobs_list = []
    salary_list = []
    for a in range(5):
        for i in range(len(data[a]['results'])):
            salary_min = data[a]['results'][i]['salary_min']
            salary_max = data[a]['results'][i]['salary_max']
            max_list.append(salary_max)
            min_list.append(salary_min)

            count = data[0]['count']
            jobs = data[a]['results'][i]['title']
            jobs_list.append(jobs)
            salary_list.append(salary_min)

    estimate = ((sum(min_list)+sum(max_list))/(len(min_list)+len(max_list))) * 0.74 #GBP conversion
    print(f"Average Salary: £{estimate:.2f}")
    print(f"Amount of Job opprtunities requiring skill(s): {count}")
    database_data = []
    for job,salary in zip(jobs_list,salary_list):
        jobsalary = (job, round(salary * 0.74, 2))
        database_data.append(jobsalary)
except IndexError:
    print("~~~~~~~Halfway~~~~~~~")

conn = sqlite3.connect("Employment.db")
conn.execute("PRAGMA foreign_keys = ON")
try:
    cursor = conn.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS Jobs(
                Job_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Job_Title TEXT NOT NULL, 
                Salary INTEGER NOT NULL
                )
                """)
    conn.commit()

    cursor.executemany("""
                    INSERT INTO Jobs (Job_Title, Salary)
                    VALUES (?, ?)
                    """, database_data)
    conn.commit()
except NameError:
    print("~~~~~~~Complete~~~~~~~")
