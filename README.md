# Анализ качества данных на Python
Данный проект, с помощью описания метрик метаданных и описания самих наборов данных, определяет для сервиса системы классификаторов Санкт-Петербурга:
### 1) Метрики метаданных:
- показатель метрики Findability (Keyword usage, Categories, Geo search, Time based search)
- показатель метрики Accessibility (AccessURL accessibility)
- показатель метрики Reusability (Contact point, Publisher)
### 2) Метрики данных, для каждого столбца:
- количество пропусков;
- количество уникальных значений;
- количество нулей (для числовых полей);
- мин/макс/среднее (для числовых полей);
### 3) Метрики для всего набора данных:
- количество строк;
- количество столбцов
## Технологии
* [python](https://www.python.org)
* [requests](https://pypi.org/project/requests/)
* [pandas](https://pypi.org/project/pandas/)
