import requests
import sqlite3
from secrets import API_KEY

# get api key from secrets.py
api_key = API_KEY

# connect to database
sql_conn = sqlite3.connect("calendarific.db")

cursor = sql_conn.cursor()

# create table
sql_query = """ CREATE TABLE IF NOT EXISTS calendarific (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    type TEXT,
    country TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER
    )"""

cur = cursor.execute(sql_query)
cur.connection.commit()

# make request to calendarific
URL = "https://calendarific.com/api/v2/holidays?api_key={}".format(
    api_key)

country = 'BR'
year = '2022'

response = requests.get(
    f"{URL}&country={country}&year={year}")

# feriados = response.get('response').get('holidays')
feriados = response.json().get('response').get('holidays')

# insert into database
for feriado in feriados:
    name = feriado.get('name')
    description = feriado.get('description')
    type = feriado.get('type')
    type = ', '.join(type)
    country = feriado.get('country').get('name')
    year = feriado.get('date').get('datetime').get('year')
    month = feriado.get('date').get('datetime').get('month')
    day = feriado.get('date').get('datetime').get('day')

    cursor.execute(
        """INSERT INTO calendarific (name, description, type, country, year, month, day) VALUES (?, ?, ?, ?, ?, ?, ?)""",  # noqa
        (name, description, type, country, year, month, day))

    cursor.connection.commit()

    print("Added {};".format(name))
print("Done.")
