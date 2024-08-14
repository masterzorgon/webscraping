from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import requests

url = 'https://registrar.web.baylor.edu/exams-grading/spring-2024-final-exam-schedule'
# Request in case 404 Forbidden error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, "html.parser")
print(soup.title.text)

tables = soup.findAll("table")

finals_table = tables[1]

rows = finals_table.findAll("tr");

myclassfile = open("class_schedule.csv", "r")

myclasses = csv.reader(myclassfile)

for rec in myclasses:
    myclass = rec[0]
    mytime = rec[1]

    for row in rows[1:]:
        td = row.findAll("td")
        sch_class = td[0].text.strip("\n")
        sch_time = td[1].text.strip("\n")
        exam_day = td[2].text.strip("\n")
        exam_time = td[3].text.strip("\n")

        if sch_class == myclass and sch_time == mytime:
            print(myclass, mytime, exam_day, exam_time)
