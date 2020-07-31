import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE data (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'chad', 'asdf')
insert_query = "INSERT INTO data VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

data = [
    (2, 'chase', 'abcd'),
    (3, 'chris', 'efgh')
]
cursor.executemany(insert_query, data)

select_query = "SELECT * FROM data"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()