import requests
from bs4 import BeautifulSoup
import sys
import re

Country_Input= input("Input the ISO 3166-1 country code of the country you would like to seacrh in?\n").lower()
Country_Codes = ('gb', 'us','at','au','be','br','ca','ch','de','es','fr','in','it','mx','nl','nz','pl','sg','za')

if Country_Input in Country_Codes:
    print("This is a valid country code")
else:
    print(f"{Country_Input} is not available/invalid")
    sys.exit()

Choice = input("(Choose option 1 or 2)\nWould like to see\n1. What your pay will be with your current skills\n2. What skills have the most pay in general")
if Choice == '1':
    Skills = input("Input your current skill(s)(if plural separate by comma): ")
    url = f"http://api.adzuna.com/v1/api/jobs/{Country_Input}/search/1?app_id=bbb231a1&app_key=ead6a75aff389175119f5fc5fd7d97cc&what={Skills}&content-type=application/json"

response = requests.get(url)
Data = response.json()

Min_List = []
Max_List = []
for i in range(len(Data['results'])):
    Salary_min = Data['results'][i]['salary_min']
    Salary_max = Data['results'][i]['salary_max']
    Max_List.append(Salary_max)
    Min_List.append(Salary_min)

Max_Estimate = sum(Max_List)/len(Max_List)
Min_Estimate = sum(Min_List)/len(Min_List)
if Max_Estimate == Min_Estimate:
    print(f"Estimated Salary is {Min_Estimate}")
else:
    print(f"Otimistic estimated salary: {Max_Estimate}")
    print(f"Conservative Estimated salary: {Min_Estimate}")