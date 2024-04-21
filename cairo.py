import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

stu_num = int(input("how many students you want : "))
start_num = int(input("where you want to start : "))

range_s=  range(start_num,(start_num+stu_num*5))

random_seat = random.sample(range_s,stu_num)


pages = [requests.get(f"https://eduserv.cairo.gov.eg/api/results/Preparatory-Certificate?SeatNumber={i}")
        for i in random_seat]
StudentData = []
headers= ['اسم الطالب','رقم الجلوس','المرحلة','الإدارة التعليمية','المدرسة','الفصل الدراسى','لغة عربية','لغة اجنبية','رياضيات','علوم','دراسات اجتماعية','المجموع الكلي']
names = ['اسم المادة','الدرجة']

def main(page,random_seat):
    src = page.content
    soup = BeautifulSoup(src,"lxml")

    data = eval(soup.find("p").contents[0])

    StudentDetails = list(data["StudentDetails"])[0]
    StudentDetails.update({'رقم الجلوس':f'{random_seat}'})
    FinalResult = list(data["FinalResult"])
    StudentData.append({headers[i]:StudentDetails[headers[i]] for i in range(6)})
    StudentData[-1].update({headers[i+5]:FinalResult[i][names[1]] for i in range(1,len(headers)-5)})

for index in range(len(random_seat)):
    main(pages[index],random_seat[index])

with open(f"results-{stu_num}.csv","w",newline="",encoding="utf-8") as out:
    dict_out = csv.DictWriter(out,headers)
    dict_out.writeheader()
    dict_out.writerows(StudentData)
    print(f"results-{stu_num}.csv created")