import pandas as pd
import requests
import json
import itertools

rang = range(1, 336, 3)
structure_versions = list() #структурные версии
names = list() #имена датасетов
tags = list() #ключевые слова
categorys = list() #категории
contact_points = list() #контактные данные
agencys = list() #поставщики 
geodata = list() #наличие геоданных

for i in rang: #версии
    url_link_ver = f'http://classif.gov.spb.ru/api/v2/datasets/{i}/versions/latest'
    response = requests.get(url_link_ver,headers ={'Authorization':'Token 52e950332c5458c889a34f705fefda906829b9dd'})
    if(response.status_code != 200):
         structure_versions.append(404)
         names.append("404")
         continue
    data_ver = response.json()
    for data in data_ver['structures']:
        structure_versions.append(data['id'])
        names.append(data['name'])

for i in rang: #паспорта
    url_link_pass = f'http://classif.gov.spb.ru/api/v2/datasets/{i}/'
    response = requests.get(url_link_pass,headers ={'Authorization':'Token 52e950332c5458c889a34f705fefda906829b9dd'})
    if(response.status_code != 200):
        tags.append(404)
        categorys.append(404)
        contact_points.append(404)
        agencys.append(404)
        geodata.append(404)
        continue
    data_pass = response.json()
    if(data_pass["tags"]):
        tags.append(data_pass["tags"])
    else:
        tags.append('Нет')
    categorys.append(data_pass['category'])
    contact_points.append(data_pass['responsible_persons'])
    agencys.append(data_pass['agency'])
    geodata.append(data_pass["has_geodata"])


j = 0
for i in rang: #данные
    findability_weight = 0
    accessibility_weight = 0
    reusability_weight = 0
    url_link = f'http://classif.gov.spb.ru/api/v2/datasets/{i}/versions/latest/data/{structure_versions[j]}/?per_page=100'
    name = names[j]
    agency = agencys[j]
    category = categorys[j]
    contact_point = contact_points[j]
    tag = tags[j]
    is_geo = geodata[j]
    j+=1
    response = requests.get(url_link,headers ={'Authorization':'Token 52e950332c5458c889a34f705fefda906829b9dd'})
    if(response.status_code != 200 or i == 61 or i == 62 or i == 63):
        continue
    accessibility_weight += 50
    data = response.json()
    posts = pd.DataFrame.from_dict(data["results"])
    print(f"{i} Датасет:", name)
    print("Кол-во строк:", posts.shape[0], "\nКол-во столбцов:", posts.shape[1])
    print("\n")
    print("Уникальные значения:")
    coords_name = ['coordinates', 'coord', 'coordinate', 'longitude', 'longitude_latitude']
    for column in posts.columns:
        for column_name in coords_name:
            if column_name == column:
                posts[column] = posts[column_name].dropna().apply(lambda x: f'({x[0]}, {x[1]})')
    print(pd.DataFrame(posts.nunique()))
    print("\n")
    print("Кол-во 0:")
    print(posts.eq(0).sum())
    print("\n")
    print("Пропуски:")
    print(posts.isna().mean()) # или count()
    print("\n")
    print("Кол-во/Мин./Макс./Ср.:")
    if (posts.select_dtypes(exclude = object).empty):
        print('Нет числовых значений')
    else:
        print(posts.describe(percentiles=[]).unstack())
    print("\n")
    print("Findability:")
    if(tag != 'Нет'):
        findability_weight += 30
    print("Ключевые слова(30):", tag)
    if(category):
        findability_weight += 30
    print("Сфера(30):", category)
    if(is_geo != False):
        findability_weight += 20
    print("Наличие геоданных(20):", is_geo)
    is_datetime = posts.columns[posts.columns.str.contains('date|time')].notna().all()
    if(is_datetime):
        findability_weight += 20
    print("Поиск по времени(20):", is_datetime)
    print("Weight:", findability_weight)
    print("\n")
    print("Accessibility:")
    print("AccessURL accessibility(50): status code -", response.status_code)
    print("Weight:", accessibility_weight)
    print("\n")
    print("Reusability:")
    if(contact_point):
        reusability_weight += 20
    print("Конт. точка(20):", contact_point)
    if(agency):
        reusability_weight += 10
    print("Издатель(10):", agency)
    print("Weight:", reusability_weight)
    print("\n")
    print("----------------------------------------------------------------")
    
