# example of how to work with sqlite

import sqlite3

# initialize connection
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# create
create_table = "CREATE TABLE users (id int, username text, password text)" # query
cursor.execute(create_table)

# insert one user
user = (1, "rolf", "asdf")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# insert many
users = [
	(2, "bob", "qwer"),
	(3, "jerry", "uiop")
]
cursor.executemany(insert_query, users)

# select
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
	print(row)

# save changes
connection.commit()

# close
connection.close()



