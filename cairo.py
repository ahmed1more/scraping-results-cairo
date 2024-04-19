import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

stu_num = int(input("how many students you want : "))
start_num = int(input("where you want to start : "))

pages = [requests.get(f"https://eduserv.cairo.gov.eg/api/results/Preparatory-Certificate?SeatNumber={i}")
        for i in range(start_num,start_num+stu_num)]
StudentData = []
headers= ['اسم الطالب','رقم الجلوس','المرحلة','الإدارة التعليمية','المدرسة','الفصل الدراسى','لغة عربية','لغة اجنبية','رياضيات','علوم','دراسات اجتماعية','المجموع الكلي']
names = ['اسم المادة','الدرجة']

def main(page,start_num,plus):
    src = page.content
    soup = BeautifulSoup(src,"lxml")

    data = eval(soup.find("p").contents[0])

    StudentDetails = list(data["StudentDetails"])[0]
    StudentDetails.update({'رقم الجلوس':f'{start_num+plus}'})
    FinalResult = list(data["FinalResult"])
    StudentData.append({headers[i]:StudentDetails[headers[i]] for i in range(6)})
    StudentData[-1].update({headers[i+5]:FinalResult[i][names[1]] for i in range(1,len(headers)-5)})

for p in range(len(pages)):
    main(pages[p],start_num,p)