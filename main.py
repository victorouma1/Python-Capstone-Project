import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st

class AverageSalary:
    def __init__(self,min,max):
        self.min = min
        self.max = max
    def uk_average(self):
        return ((sum(self.min)+sum(self.max))/(len(self.min)+len(self.max))) * 0.74
    def ke_average(self):
        return (self.min + self.max)/2

st.header("Job Market Mapper")

if "show_skills_form" not in st.session_state:
    st.session_state.show_skills_form = False

if "country" not in st.session_state:
    st.session_state.country = None

with st.form("my_form"):
    st.write("What country would you like to search from?")
    col1, col2 = st.columns(2)

    with col1:
        kenya = st.form_submit_button("Kenya")
    with col2:
        uk = st.form_submit_button("UK")

    if kenya:
        st.session_state.country = "Kenya"
    if uk:
        st.session_state.country = "UK"

with st.form("my_form1"):
    city_streamlit = st.text_input("What city would you like to search from? ")
    submitted = st.form_submit_button("Submit")

city = city_streamlit.title()
if submitted:
    st.success(f"City set to: {city}")

st.write("### What would you like to see?")
    
data = []
data1 = []
data2 = []

if st.session_state.country == "UK":
    if st.button('1. What your pay will be with your current skills'):
        st.session_state.show_skills_form = True
    if st.session_state.show_skills_form:
        with st.form("my_form2"):
            skills = st.text_input("Input your desired role or current skill(s)(if plural separate by a space): ")
            submit = st.form_submit_button("Submit")

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
            

    if st.button('2. What skills are in demand'):
        st.session_state.show_skills_form = True
        skills = ["Python", "SQL", "Machine Learning", "AWS", "Java","JavaScript","C++","CSS","HTML","MATLAB","AI","Power BI"]
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
if st.session_state.country == "Kenya":
    with st.form("my_form3"):
        role = st.text_input("Input your desired role: ")
        submission = st.form_submit_button("Submit")

    url1 = "https://jsearch.p.rapidapi.com/estimated-salary"

    query_string = {"job_title":f"{role}","location":f"{city}","location_type":"ANY","years_of_experience":"ALL"}

    headers = {
	    "x-rapidapi-key": "afe3bf38femsh5c889fa2fbf37d7p1f69dbjsn23f92942daf6",
	    "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url1, headers=headers, params=query_string)

    data2.append(response.json())

    try:
        min_salary1 = data2[0]['data'][0]['min_base_salary'] # in KES
        max_salary1 = data2[0]['data'][0]['max_base_salary'] 
        job_title1 = data2[0]['parameters']['job_title'] 
        publisher_link = data2[0]['data'][0]['publisher_link']

        pattern1 = r"\d{4}-\d{2}-\d{2}"
        date_text1 = data2[0]['data'][0]['salaries_updated_at']
        date_find = re.findall(pattern1, date_text1)
        date1 = date_find[0]

        processing = {
            "Job Title": job_title1,
            "Minimum Salary (KSH)": min_salary1,
            "Maximum Salary (KSH)": max_salary1,
            "Date Posted": date1,
            "Publisher Link": publisher_link
        }

        average_obj = AverageSalary(min_salary1, max_salary1)

        average_salary = average_obj.ke_average()
        amount = len(data2)

        st.write(f"Average salary: Ksh {average_salary}")
        st.write(f"Amount of opportunities: {amount}")

        dataframe_1 = pd.DataFrame(processing, index=[0])
        st.dataframe(dataframe_1)
    
    except IndexError:
        st.write(f"{role} is not available in database ")

try:
    data_frame = pd.DataFrame(total_skill_counts.items(), columns=['Skill', 'Count'])
    st.dataframe(data_frame)
except NameError:
    print("Data Loaded Successfully")

try:
    min_list = []
    max_list = []
    jobs_list = []
    salary_list = []
    date_list = []
    company_list = []
    description_list = []
    url_list = []
    pattern = r"\d{4}-\d{2}-\d{2}"
    for a in range(5):
        sorted_jobs = sorted(
        data[a]['results'], 
        key=lambda x: datetime.fromisoformat(x['created']), 
        reverse=True
        )  
        for i in range(len(data[a]['results'])):

            redirect_url = sorted_jobs[i]['redirect_url']
            url_list.append(redirect_url)

            salary_min = sorted_jobs[i]['salary_min']
            salary_max = sorted_jobs[i]['salary_max']
            
            max_list.append(salary_max)
            min_list.append(salary_min)

            date_text = sorted_jobs[i]['created']
            date = re.findall(pattern, date_text)
            date_list.append(date[0])

            count = data[0]['count']
            jobs = sorted_jobs[i]['title']
            company = sorted_jobs[i]['company']['display_name']
            description = sorted_jobs[i]['description']

            jobs_list.append(jobs)
            salary_list.append(f"{round(salary_min, 2)} - {round(salary_max, 2)}")
            company_list.append(company)
            description_list.append(description)

    estimate_obj = AverageSalary(min_list, max_list)
    estimate = estimate_obj.uk_average()
    st.write(f"Average Salary: £{estimate:.2f}")
    st.write(f"Amount of Job opprtunities requiring skill(s): {count}")

    database_data = []
    for job,salary,dates,company,redirect in zip(jobs_list,salary_list,date_list,company_list,url_list):
        job_data = (job,salary, dates,company, redirect)
        database_data.append(job_data)
except IndexError:
    print("Halfway")

try:
    conn = sqlite3.connect("Employment.db")
    conn.execute("PRAGMA foreign_keys = ON")

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Jobs")
    conn.commit()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS Jobs(
                Job_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Job_Title TEXT NOT NULL, 
                Salary_GBP TEXT NOT NULL,
                Date_Posted DATE NOT NULL,
                Company TEXT NOT NULL,
                URL TEXT NOT NULL
                )
                """)
    conn.commit()

    cursor.executemany("""
                    INSERT INTO Jobs (Job_Title, Salary_GBP, Date_Posted, Company, URL)
                    VALUES (?, ?, ?, ?, ?)
                    """, database_data)
    conn.commit()
except NameError:
    print("Complete")

st.sidebar.title("App Menu")
page = st.sidebar.selectbox("Select a Page", ["Home", "Database Viewer"])

if page == "Home":
    st.write("Select 'Database Viewer' in the sidebar to see the data.")
    st.write("Click on the Job title to see description. ")

if page == "Database Viewer":
    st.write("### Database Explorer")

    database_path = "Employment.db" 
    try:
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(tables_query, conn)

        if not tables.empty:
            table_name = st.selectbox("Select a table to view", tables['name'])
            
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            st.write(f"{table_name} table")
            event = st.dataframe(
                df, 
                on_select="rerun", 
                selection_mode="single-row",
                use_container_width=True
            )
            if len(event.selection.rows) > 0:
                selected_row_index = event.selection.rows[0]
                display = description_list[selected_row_index]

                st.write(f"Description: {display}")

        else:
            st.warning("The database is empty (no tables found).")
            
        conn.close()

    except Exception as e:
        st.error(f"Error connecting to database: {e}")
