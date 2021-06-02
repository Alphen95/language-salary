import requests, datetime, os
from pprint import pprint
from terminaltables import AsciiTable
from dotenv import load_dotenv
java = {"hh":[0,0],"sj":[0,0]}
javascript = {"hh":[0,0],"sj":[0,0]}
ruby = {"hh":[0,0],"sj":[0,0]} 
c = {"hh":[0,0],"sj":[0,0]} 
py = {"hh":[0,0],"sj":[0,0]} 
go = {"hh":[0,0],"sj":[0,0]}
languages = ["Python","Java","C","Ruby","Javascript","Go"]
load_dotenv(".env")
superjob_header = {
    "X-Api-App-Id":os.getenv("SUPERJOB_KEY")
}


def predict_salary(min_salary,max_salary):
    if min_salary == None:
        predicted_salary = max_salary*0.8
    elif max_salary == None:
        predicted_salary = min_salary*1.2
    else:
        predicted_salary = (min_salary+max_salary)/2
    return predicted_salary

for language in languages:
    for page in range(0,20):
        job_params = {
        "per_page":100,
        "text":"Программист {}".format(language),
        "page":page,
        "area":1,
        "only_with_salary":True,
        "period":30
        }

        request = requests.get("https://api.hh.ru/vacancies",params=job_params)
        request.raise_for_status()
        for job in request.json()["items"]:
            if "Javascript" in job["name"]:
                javascript["hh"][0] += 1
                javascript["hh"][1] += predict_salary(job["salary"]["from"],job["salary"]["to"]) if job["salary"]["currency"] == "RUR" else 0
            elif "Java" in job["name"]:
                java["hh"][0] += 1
                java["hh"][1] += predict_salary(job["salary"]["from"],job["salary"]["to"]) if job["salary"]["currency"] == "RUR" else 0
            elif "Python" in job["name"]:
                py["hh"][0] += 1
                py["hh"][1] += predict_salary(job["salary"]["from"],job["salary"]["to"]) if job["salary"]["currency"] == "RUR" else 0
            elif "C" in job["name"]:
                c["hh"][0] += 1
                c["hh"][1] += predict_salary(job["salary"]["from"],job["salary"]["to"]) if job["salary"]["currency"] == "RUR" else 0
            elif "Ruby" in job["name"]:
                ruby["hh"][0] += 1
                ruby["hh"][1] += predict_salary(job["salary"]["from"],job["salary"]["to"]) if job["salary"]["currency"] == "RUR" else 0
            elif "Go" in job["name"]:
                go["hh"][0] += 1
                go["hh"][1] += predict_salary(job["salary"]["from"],job["salary"]["to"]) if job["salary"]["currency"] == "RUR" else 0      

for language in languages:
    for page in range(0,20):
        superjob_params ={
            "keywords":["Программист {}".format(language)],
            "town":"Москва",
            "count":100,
            "page":page
        }
        request = requests.get("https://api.superjob.ru/2.33/vacancies/",headers=superjob_header,params=superjob_params)
        request.raise_for_status()
        superjob_vacancies =request.json()
        for job in superjob_vacancies["objects"]:
            if "Javascript" in job["profession"]:
                javascript["sj"][0] += 1
                javascript["sj"][1] += predict_salary(job["payment_from"] if job["currency"] =="rub" else None,job["payment_to"] if job["currency"] =="rub" else None)
            elif "Java" in job["profession"]:
                java["sj"][0] += 1
                java["sj"][1] += predict_salary(job["payment_from"] if job["currency"] =="rub" else None,job["payment_to"] if job["currency"] =="rub" else None)
            elif "Python" in job["profession"]:
                py["sj"][0] += 1
                py["sj"][1] += predict_salary(job["payment_from"] if job["currency"] =="rub" else None,job["payment_to"] if job["currency"] =="rub" else None)
            elif "C" in job["profession"]:
                c["sj"][0] += 1
                c["sj"][1] += predict_salary(job["payment_from"] if job["currency"] =="rub" else None,job["payment_to"] if job["currency"] =="rub" else None)
            elif "Ruby" in job["profession"]:
                ruby["sj"][0] += 1
                ruby["sj"][1] += predict_salary(job["payment_from"] if job["currency"] =="rub" else None,job["payment_to"] if job["currency"] =="rub" else None)
            elif "Ruby" in job["profession"]:
                go["sj"][0] += 1
                go["sj"][1] += predict_salary(job["payment_from"] if job["currency"] =="rub" else None,job["payment_to"] if job["currency"] =="rub" else None)            

py["hh"][1] //= py["hh"][0] if py["hh"][0] > 0 else 1
c["hh"][1] //= c["hh"][0] if c["hh"][0] > 0 else 1
java["hh"][1] //= java["hh"][0] if java["hh"][0] > 0 else 1
javascript["hh"][1] //= javascript["hh"][0] if javascript["hh"][0] > 0 else 1
ruby["hh"][1] //= ruby["hh"][0] if ruby["hh"][0] > 0 else 1
go["hh"][1] //= go["hh"][0] if go["hh"][0] > 0 else 1
   
py["sj"][1] //= py["sj"][0] if py["sj"][0] > 0 else 1
c["sj"][1] //= c["sj"][0] if c["sj"][0] > 0 else 1
java["sj"][1] //= java["sj"][0] if java["sj"][0] > 0 else 1
javascript["sj"][1] //= javascript["sj"][0] if javascript["sj"][0] > 0 else 1
ruby["sj"][1] //= ruby["sj"][0] if ruby["sj"][0] > 0 else 1
go["sj"][1] //= go["sj"][0] if go["sj"][0] > 0 else 1
table_data_sj = [
    ["Язык","Вакансий найдено","Средняя зарплата"],
    ["C",c["sj"][0],c["sj"][1]],
    ["Go",go["sj"][0],go["sj"][1]],
    ["Python",py["sj"][0],py["sj"][1]],
    ["Ruby",ruby["sj"][0],ruby["sj"][1]],
    ["Java",java["sj"][0],java["sj"][1]],
    ["Javascript",javascript["sj"][0],javascript["sj"][1]]
]
table_data_hh = [
    ["Язык","Вакансий найдено","Средняя зарплата"],
    ["C",c["hh"][0],c["hh"][1]],
    ["Go",go["hh"][0],go["hh"][1]],
    ["Python",py["hh"][0],py["hh"][1]],
    ["Ruby",ruby["hh"][0],ruby["hh"][1]],
    ["Java",java["hh"][0],java["hh"][1]],
    ["Javascript",javascript["hh"][0],javascript["hh"][1]]
]
table_sj = AsciiTable(table_data_sj,"SuperJob Moscow")
table_hh = AsciiTable(table_data_hh,"HeadHunter Moscow")
print(table_sj.table)
print(table_hh.table)