import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_users_table = 'create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)'

create_items_table = 'create table if not exists items (id INTEGER PRIMARY KEY, name text, price real)'

cursor.execute(create_users_table)
cursor.execute(create_items_table)

# insert_query = 'insert into users values (null, ?, ?)'
# user = ("john", "asdf")
#
# cursor.execute(insert_query, user)
#
# users = [
#     ("clark", "pop"),
#     ("anna", "mnm"),
# ]
#
# cursor.executemany(insert_query, users)
#
# users_query = 'select * from users'
#
# for row in cursor.execute(users_query):
#     print(row)

connection.commit()

connection.close()