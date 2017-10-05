# the hard code way to create database

import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cur.execute(create_user_table)

create_item_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cur.execute(create_item_table)

cur.execute("INSERT INTO items (name, price) VALUES ('chair', 15.99)")

conn.commit()
conn.close()
