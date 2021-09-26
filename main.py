#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
from terminaltables import SingleTable
from dotenv import load_dotenv


def predict_salary(min_salary, max_salary):
    if not min_salary:
        predicted_salary = max_salary * 0.8
    elif not max_salary:
        predicted_salary = min_salary * 1.2
    else:
        predicted_salary = (min_salary + max_salary) / 2
    return predicted_salary


def main():
    jobs = []
    salaries = {
        'Java': {'hh': [0, 0, 0], 'sj': [0, 0, 0]},
        'Javascript': {'hh': [0, 0, 0], 'sj': [0, 0, 0]},
        'Ruby': {'hh': [0, 0, 0], 'sj': [0, 0, 0]},
        'C': {'hh': [0, 0, 0], 'sj': [0, 0, 0]},
        'Python': {'hh': [0, 0, 0], 'sj': [0, 0, 0]},
        'Go': {'hh': [0, 0, 0], 'sj': [0, 0, 0]},
        }

    programmer_job_id = None
    languages = [
        'Python',
        'Java',
        'C',
        'Ruby',
        'Javascript',
        'Go',
        ]

    for language in languages:
        for page in range(0, 20):
            job_params = {
                'per_page': 100,
                'text': 'Программист {}'.format(language),
                'page': page,
                'area': 1,
                'only_with_salary': True,
                'period': 30,
                }

            request = requests.get('https://api.hh.ru/vacancies',
                                   params=job_params)
            request.raise_for_status()
            request_items = request.json()['items']
            for job in request_items:
                jobs.append(job)
    for job in jobs:
        for language in languages:
            if language in job['name']:
                salaries[language]['hh'][0] += 1
                salaries[language]['hh'][1] += \
                    (predict_salary(job['salary']['from'], job['salary'
                     ]['to']) if job['salary']['currency'] == 'RUR'
                      else 0)
                salaries[language]['hh'][2] += (1 if job['salary'
                        ]['currency'] == 'RUR' else 0)

    superjob_header = \
        {'X-Api-App-Id': 'v3.r.134393368.365b3beb5013c1ab2d4d7e9e1e0808cec6c655df.4bf372ba86e1dc70c61ed378319c0dc9857ed6d9'}
    jobs = []
    for language in languages:
        for i in range(0, 20):
            superjob_params = {
                'keywords': ['Программист {}'.format(language)],
                'town': 'Москва',
                'count': 100,
                'page': i,
                }
            request = \
                requests.get('https://api.superjob.ru/2.33/vacancies/',
                             headers=superjob_header,
                             params=superjob_params)
            request.raise_for_status()
            superjob_vacancies = request.json()['objects']
            for job in superjob_vacancies:
                jobs.append(job)
    for job in jobs:
        for language in languages:
            if language in job['profession']:
                salaries[language]['sj'][0] += 1
                salaries[language]['sj'][1] += \
                    predict_salary((job['payment_from'
                                   ] if job['currency'] == 'rub'
                                    else None), (job['payment_to'
                                   ] if job['currency'] == 'rub'
                                    else None))
                salaries[language]['sj'][2] += (1 if job['currency']
                        == 'rub' else 0)
    for language in salaries.items():
        language[1]['hh'][1] //= (language[1]['hh'
                                  ][0] if language[1]['hh'][0]
                                  > 0 else 1)
        language[1]['sj'][1] //= (language[1]['sj'
                                  ][0] if language[1]['sj'][0]
                                  > 0 else 1)
        salaries[language[0]] = language[1]
    table_data_sj = ["Язык","Вакансий найдено","Вакансий обработано","Средняя зарплата"]
    for language in salaries.items():
        table_data_sj.append([language[0], language[1]['sj'][0],
                             language[1]['sj'][2], language[1]['sj'
                             ][1]])
    table_data_hh = ["Язык","Вакансий найдено","Вакансий обработано","Средняя зарплата"]
    for language in salaries.items():
        table_data_hh.append([language[0], language[1]['hh'][0],
                             language[1]['hh'][2], language[1]['hh'
                             ][1]])
    table_sj = SingleTable(table_data_sj, 'SuperJob Moscow')
    table_hh = SingleTable(table_data_hh, 'HeadHunter Moscow')
    print(table_sj.table)
    print(table_hh.table)


main()